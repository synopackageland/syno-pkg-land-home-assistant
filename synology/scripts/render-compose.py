#!/usr/bin/env python3
"""Render the unmodified official image with the package's nonroot adapter."""
import base64
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
COMPONENT_SHA256 = 'e5badaaacaa63cfd6fe733924a05e76d75058836190398598fb24de57cd47ccd'
IMAGE = 'homeassistant/home-assistant:2026.10.4@sha256:23f4dfbb69ce76315dbc4de7915504f1c2dcecd7ca2648113a493a385972e133'


def render():
    component = (ROOT / 'vendor/hass-oidc-auth-1.2.1.zip').read_bytes()
    if hashlib.sha256(component).hexdigest() != COMPONENT_SHA256:
        raise ValueError('Component checksum mismatch')
    source = (ROOT / 'container/bootstrap.py').read_text()
    bootstrap = 'COMPONENT_ARCHIVE_BASE64 = ' + repr(base64.b64encode(component).decode()) + '\n' + source
    compose = {'services': {'web': {
        'image': IMAGE,
        'entrypoint': ['python3', '-c'], 'command': [bootstrap],
        'environment': {'TZ': 'UTC', 'PYTHONDONTWRITEBYTECODE': '1'},
        'read_only': True, 'volumes': ['data:/var/tmp'],
        'tmpfs': ['/tmp:mode=1777'], 'restart': 'unless-stopped',
        'stop_grace_period': '60s',
    }}, 'volumes': {'data': {}}}
    return json.dumps(compose, indent=2) + '\n'


if __name__ == '__main__':
    result = render()
    target = ROOT / 'compose.yaml'
    if '--check' in sys.argv:
        if target.read_text() != result:
            raise SystemExit('Run python3 scripts/render-compose.py')
    else:
        target.write_text(result)
