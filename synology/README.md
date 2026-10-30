# Home Assistant for Synology DSM

## Current package

Version **2026.10.4-0002** uses published SDK/App **0.38.2**, templates
**0.35.5**, CLI **0.41.9** and executor **v0.38.2**. Protected executors require
administrator approval after upgrading. Device and mobile-client acceptance
are separate from the offline package gates.

## Mobile and native clients

`identity_gateway.upstream_auth_paths` is exactly:

```text
/api
/auth/token
/auth/revoke
```

These fixed prefixes are case-sensitive and match complete path segments.
They bypass DSM admission and keep upstream authentication and authorization.
All other paths, including browser entry, retain the existing DSM gate.

Clients with existing Home Assistant credentials can use `/api` (including
REST, `/api/websocket` and webhooks), `/auth/token` and `/auth/revoke` through the
gateway HTTPS origin. Home Assistant validates access/refresh tokens; webhook
endpoints retain their upstream secret and authorization rules.
Manage and revoke native tokens in Home Assistant; DSM logout does not revoke
them. Browser UI and interactive OIDC entry remain DSM-gated. `/auth/providers`
and `/auth/login_flow` are not exceptions. Companion first-login/onboarding and
end-to-end native-client operation remain unverified.

Home Assistant 2026.10.4, packaged as `SynoPkgHomeAssistant` 2026.10.4-0002.
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
loopback-only HTTP configuration in place. On first onboarding, the adapter uses
Home Assistant's native location detection and saves country, time zone, units
and available location/currency defaults through its core configuration API.
These are IP-based suggestions, not DSM regional settings; VPNs and proxies may
affect them. Review them in **Settings > System > General**. If detection is
unavailable, startup continues and the log requests manual setup; the country
repair remains until a country is set. Completed onboarding is not reconfigured
on subsequent starts.

HTTP YAML is used only for the private bootstrap listener. Before the serving
restart, the adapter removes that temporary block, leaving the native HTTP
store responsible for loopback binding, forwarded headers and the trusted
loopback proxy. The serving start clears the HTTP YAML migration repair.
Existing installations that already completed bootstrap are not migrated by
this fresh-install fix.

Ports 8123/8124 are reserved for loopback runtime/bootstrap. The install wizard
selects the gateway HTTPS port (default 8125) and the OIDC issuer port (default
8126); the adapter reads the selected issuer port at every start. Upgrades keep
the selected ports; reinstall to change them.

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

Use Node 22.12+ and Go 1.26.10, plus authorised access to the SDK Go module.
Never put access tokens in this repository. SDK/App are pinned to published 0.38.2, templates to 0.35.5 and CLI to 0.41.9; source overrides are not used for release builds.

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

## App-open smoke

`npm run e2e:smoke` runs the CLI's `appOpenSmoke` against an authorized NAS
with the ready marker `#continue-on-this-device`. hass-oidc-auth renders it only
after DSM admission and a successful OIDC callback; one click on it then opens
the Home Assistant UI, which the helper cannot perform. It covers a DSM administrator (A), a real
non-administrator (N, which must see the SDK access-denied page because the App
is `entry: admin-only`) and a signed-out browser (X). Install Chromium once with
`npx @e2e-dev/web install chromium`, then set `DSM_E2E_URL` (the DSM HTTPS URL),
`DSM_E2E_ACCOUNT_ADMIN` and `DSM_E2E_ACCOUNT_NORMAL` (mode 600 account JSON files
outside this repository), `DSM_E2E_PROFILE_DIR` and `DSM_E2E_OUTPUT_DIR` (under
the ignored `.e2e/`). The CLI accepts self-signed DSM and gateway certificates.
The smoke never installs packages or changes accounts; never widen the entry to
make N reach the App.

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
