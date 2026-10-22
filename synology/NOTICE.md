# Third-party software and source

- Home Assistant Core 2026.10.2: Apache-2.0; copyright the Home Assistant authors.
  Source: https://github.com/home-assistant/core/tree/2026.10.2 .
  Official image: `homeassistant/home-assistant:2026.10.2`, pinned in
  `scripts/render-compose.py`. The container retains its upstream dependency
  inventory and licenses. The source fork preserves the matching upstream tag.
  License: `LICENSES/Home-Assistant-Apache-2.0.txt`.
- hass-oidc-auth 1.2.1: MIT; copyright Christiaan Goossens and contributors.
  Source: https://github.com/christiaangoossens/hass-oidc-auth/tree/v1.2.1 .
  The unmodified release ZIP is vendored in `vendor/` and embedded into the
  generated adapter. SHA-256:
  `e5badaaacaa63cfd6fe733924a05e76d75058836190398598fb24de57cd47ccd`.
  License: `LICENSES/hass-oidc-auth-MIT.txt`. Its manifest declares aiofiles,
  Jinja2 and joserfc, which Home Assistant installs using its normal dependency
  mechanism; their upstream licenses apply. They are not bundled in the SPK.
- Synopkgland SDK/App, CLI and templates 0.23.0: MIT; synopkgland contributors.
  Generated SPK notices include the SDK and runtime dependencies.
- DSM packaging in `synology/`: MIT; Copyright (c) 2026 synopackageland.

The package does not modify upstream Home Assistant or hass-oidc-auth source.

## Package icon attribution

Official Home Assistant artwork from home-assistant/assets at `8d4090f492d60841a0db4b3b26585184b29333ba`, `logo/home-assistant-logo.zip!home-assistant-logomark-with-margins-color-on-light.png`.
Source: https://raw.githubusercontent.com/home-assistant/assets/8d4090f492d60841a0db4b3b26585184b29333ba/logo/home-assistant-logo.zip
Original SHA-256: `78a2f4e5dc994f57ec5cfaaf4d516868b144f8e1733a4c665c66093e7cbe5a22`.
License: CC-BY-NC-SA-4.0; Open Home Foundation trademark. The original asset is preserved; only size conversion/rasterization is performed for DSM. Upstream names and trademarks remain with their respective owners; this community integration does not claim upstream endorsement.
The logo is the property/trademark of the Open Home Foundation. Preserve the upstream logo guidelines and noncommercial terms in LICENSES/HomeAssistant-Logo-CC-BY-NC-SA-4.0.md and LICENSES/HomeAssistant-Logo-Guidelines.md; do not apply the Core Apache-2.0 code license to the logo.
