"""Checks runnable without private SDK access or a NAS."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('render', ROOT / 'scripts/render-compose.py')
RENDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RENDER)


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
