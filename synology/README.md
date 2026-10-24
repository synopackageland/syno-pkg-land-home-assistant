# Home Assistant for Synology DSM

## SDK 0.29.1 rebuild

Rebuild 2026.10.2-0005 with SDK/App 0.29.1 and CLI/templates 0.29.0, retaining executor/v0.27.0. Upstream images and App configuration are unchanged. No NAS testing was performed for this rebuild.

## SDK 0.28.0 rebuild

Rebuild 2026.10.2-0004 with published SDK/App/CLI/templates 0.28.0 (executor/v0.27.0), UI 0.14.4 and Go 1.26.10, with the SDK's slow-NAS startup defaults (generous health/readiness timing and a Starting status in the UI). Maintainer: Syno Package Land. Official images and application sources are unchanged. Not tested on a NAS.

2026.10.2-0004 使用已發佈 SDK/App/CLI/templates 0.28.0（executor/v0.27.0）、UI 0.14.4 與 Go 1.26.10 重建，並採用 SDK 針對慢速 NAS 的啟動預設值（較寬鬆的健康檢查／就緒時間，以及 UI 的「啟動中」狀態）；維護者顯示為 Syno Package Land。 官方映像與上游程式維持原樣。尚未在 NAS 上測試。

## SDK 0.26.0 rebuild

Rebuild 2026.10.2-0003 with published SDK/App/CLI/templates 0.26.0, UI 0.14.4 and Go 1.26.10. Maintainer: Syno Package Land. Official images and application sources are unchanged.

2026.10.2-0003 使用已發佈 SDK/App/CLI/templates 0.26.0、UI 0.14.4 與 Go 1.26.10 重建；維護者顯示為 Syno Package Land。 官方映像與上游程式維持原樣。

Home Assistant 2026.10.2, packaged as `SynoPkgHomeAssistant` 2026.10.2-0001.
This is a community package, not an official Home Assistant or Synology product.
Upstream source and the official container image remain unchanged. All packaging
lives in this directory. The official Docker Hub image is pinned by version and its multi-platform index SHA-256. The x86_64 manifest matches the official GHCR image byte for byte.

## Requirements and support

- DSM 7.2.1 or later on x86_64, with Container Manager installed.
- The container runs as the package account, without root or broad capabilities.
- Host networking supports mDNS through the declared UDP 5353 listener.
- SSDP and integrations requiring random UDP ports are unsupported. Bluetooth,
  USB devices, Supervisor, add-ons and Home Assistant OS features are unsupported.
- Internet access is needed to pull the official image and install the pinned
  OIDC component's declared Python dependencies on first start.
- Mobile Companion App sign-in is unverified. Browser acceptance does not certify it.
- Only the tested DSM release and architecture are certified by the release's
  acceptance notes; other DSM versions remain unverified.

## DSM sign-in

Open **Home Assistant** from DSM's main menu. The SDK handles DSM sign-in and
OIDC; no separate App password or external identity server is required. Open the
same install by its IP address or a trusted DNS alias. Each origin has separate
host-only cookies and requires its own DSM session. Use trusted DNS and TLS.

This release admits **DSM administrators only**. Each admitted principal maps to
an upstream Home Assistant administrator through the pinned OIDC integration.
Ordinary DSM users receive HTTP 403, even if Application Privileges allows them.
General-user admission and live role demotion have not been certified, so general-user
admission is not enabled. DSM logout, account removal or a role change does not
immediately revoke existing Home Assistant sessions or API tokens; manage those
in Home Assistant. Removing a DSM account does not delete its Home Assistant data. Do not change the manifest gate as a substitute for testing.

The adapter completes native onboarding with a randomly generated, package-private
bootstrap owner. Its credential is never delivered to a browser; the temporary
bootstrap refresh token is deleted after HTTP configuration is confirmed. DSM
OIDC administrators are not that bootstrap owner. Upstream owner-only operations
are consequently unavailable through the DSM login. Keep the OIDC integration and
loopback-only HTTP configuration in place. First-run country/location setup remains yours to configure. Home Assistant may
show its country and HTTP YAML migration repair prompts; the adapter verifies
the promoted native HTTP settings rather than relying on migrated YAML.

Ports 8123/8124 are reserved for
loopback runtime/bootstrap, 8125 for gateway HTTPS, and 8126 for the OIDC issuer.

## Data and removal

Configuration, dashboards, automations and the database live in the package's
named volume and survive stop/start. Export backups before removal or replacing
the package; this release does not certify an upgrade from an older package.
Container Manager named volumes remain after **both** uninstall choices, including
the wizard option to delete package data. That option does not delete the named
volume containing Home Assistant configuration and its database. Back up first;
remove a retained volume explicitly through Container Manager only when its
contents are no longer needed. Reinstall retention is not a substitute for a backup.
The package has no host shared-folder mounts and does not inherit a signed-in
user's NAS filesystem permissions. This release enables no ctl/AI-control endpoint.

## Build and review

Use Node 22.12+ and Go 1.26.9, plus authorised access to the SDK Go module.
Never put access tokens in this repository. SDK/App, CLI and templates are pinned
to published 0.28.0; source overrides are not used for release builds.

```sh
cd synology
npm ci
python3 scripts/render-compose.py --check
npm test
npm run check
npm run build
node_modules/.bin/synopkgland inspect dist/*.spk --json
```

Read [the license inventory](NOTICE.md) and [CI policy](docs/ci.md).

## Upstream maintenance

Keep an `upstream` remote pointing to `https://github.com/home-assistant/core`.
Pause repository Actions using the procedure in `docs/ci.md`, then use
`bash synology/upgrade.sh <stable-tag> <increasing-build-number>` from a clean
checkout with this directory's pinned CLI on PATH. The command merges the exact
upstream tag, preserves upstream files, pins the official image in
`compose.image.yaml`, and checks/builds the package. Review and commit the result,
repeat device acceptance, then apply the CI allowlist policy before publication.
Upgrades are not certified by this first package release.

## Official package icon

The DSM package uses the official project artwork, preserved unchanged and only resized/rasterized to the required icon sizes. See [assets/icon-source.json](assets/icon-source.json) for the source revision and original SHA-256, and [NOTICE.md](NOTICE.md) for attribution and the applicable image license. The package ID remains `SynoPkgHomeAssistant` for upgrade continuity.
