"""Checks runnable without private SDK access or a NAS."""
import ast
from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import AsyncMock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('render', ROOT / 'scripts/render-compose.py')
RENDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RENDER)


def adapter_functions(**globals_: object) -> dict:
    tree = ast.parse((ROOT / 'container/bootstrap.py').read_text())
    tree.body = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
    namespace = {'json': json, **globals_}
    exec(compile(tree, '<adapter functions>', 'exec'), namespace)
    return namespace


class BootstrapDefaults(unittest.IsolatedAsyncioTestCase):
    async def test_detected_region_is_saved_through_native_api(self) -> None:
        settings = {'country': 'US', 'time_zone': 'America/New_York', 'unit_system': 'us_customary',
                    'currency': 'USD', 'latitude': 40.7, 'longitude': -74.0}
        ws = AsyncMock(side_effect=[{'success': True, 'result': {**settings, 'ip': 'redacted'}},
                                    {'success': True}])
        await adapter_functions()['configure_core_defaults'](ws)
        self.assertEqual(ws.await_args_list[0].args, (8124, 'config/core/detect'))
        self.assertEqual(ws.await_args_list[1].args, (8124, 'config/core/update'))
        self.assertEqual(ws.await_args_list[1].kwargs, settings)

    async def test_detection_failures_request_manual_setup(self) -> None:
        for response in ({'success': True, 'result': {}}, {'success': False}, TimeoutError()):
            with self.subTest(response=response):
                ws = AsyncMock(side_effect=[response])
                output = io.StringIO()
                with redirect_stdout(output):
                    await adapter_functions()['configure_core_defaults'](ws)
                ws.assert_awaited_once_with(8124, 'config/core/detect')
                self.assertIn('Settings > System > General', output.getvalue())

    async def test_rejected_core_update_refuses_completion(self) -> None:
        ws = AsyncMock(side_effect=[{'success': True, 'result': {'country': 'TW'}},
                                    {'success': False}])
        with self.assertRaisesRegex(RuntimeError, 'Core configuration failed'):
            await adapter_functions()['configure_core_defaults'](ws)

    def test_removing_http_yaml_preserves_user_config_and_native_store(self) -> None:
        with TemporaryDirectory() as directory:
            conf = Path(directory) / 'configuration.yaml'
            store = Path(directory) / 'http'
            store.write_text('{"data":{"stable":{"server_port":8123}}}')
            stored = store.read_bytes()
            retained = {'homeassistant': {'country': 'TW'}, 'automation': [{'alias': 'Keep me'}]}
            conf.write_text(json.dumps({**retained, 'http': {'server_port': 8124}}))
            conf.chmod(0o600)
            remove = adapter_functions()['remove_http_yaml']
            remove(conf)
            remove(conf)
            self.assertEqual(json.loads(conf.read_text()), retained)
            self.assertEqual(conf.stat().st_mode & 0o777, 0o600)
            self.assertEqual(store.read_bytes(), stored)

    def test_private_http_refuses_incompatible_native_policy(self) -> None:
        private = {'server_host': ['127.0.0.1'], 'server_port': 8123,
                   'use_x_forwarded_for': True, 'trusted_proxies': ['127.0.0.1/32']}
        with TemporaryDirectory() as directory:
            store = Path(directory) / 'http'
            check = adapter_functions(http_store=store)['assert_private_http']
            store.write_text(json.dumps({'data': {'stable': private, 'pending': None}}))
            check(final=True)
            for changed in ({'server_host': ['0.0.0.0']}, {'server_port': 8124},
                            {'use_x_forwarded_for': False}, {'trusted_proxies': ['0.0.0.0/0']}):
                with self.subTest(changed=changed):
                    store.write_text(json.dumps({'data': {'stable': {**private, **changed}}}))
                    with self.assertRaisesRegex(RuntimeError, 'HTTP policy is incompatible'):
                        check(final=True)


class BootstrapBoundary(unittest.TestCase):
    def test_rejects_root_before_touching_data(self):
        self.assert_refused(0, '127.0.0.1')

    def test_rejects_wildcard_before_touching_data(self):
        self.assert_refused(1000, '0.0.0.0')

    def assert_refused(self, uid, bind):
        source = (ROOT / 'container/bootstrap.py').read_text()
        program = f'import os; os.getuid = lambda: {uid}; os.environ["HA_BIND"] = {bind!r}; exec({source!r})'
        result = subprocess.run([sys.executable, '-c', program], capture_output=True, text=True, timeout=5)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')
        self.assertIn('requires package UID and SDK loopback listener', result.stderr)

    def test_rendered_adapter_is_current_and_compiles(self):
        import json
        rendered = RENDER.render()
        self.assertEqual((ROOT / 'compose.yaml').read_text(), rendered)
        command = json.loads(rendered)['services']['web']['command'][0]
        compile(command, '<container adapter>', 'exec')

    def test_vendored_component_is_checked_before_embedding(self):
        from unittest.mock import patch
        with patch.object(RENDER.hashlib, 'sha256') as digest:
            digest.return_value.hexdigest.return_value = 'invalid'
            with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
                RENDER.render()
