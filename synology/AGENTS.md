# Packaging scope

These instructions govern DSM packaging under `synology/`. Keep upstream source
unchanged. For package-only work, use this directory's `npm test`, render check,
and published CLI check/build/inspect gates; upstream `script/setup` and full
upstream lint/test commands apply when upstream product source is changed.
Read `docs/ci.md` before changing the owned workflow or updating an upstream tag.

# Compose App development

Run `synopkgland skill list`, then `synopkgland skill show orchestrator`,
`synopkgland skill show compose` and `synopkgland skill show upstream-fork`.
Prefer `check --json`, `build --json`, `inspect <spk> --json` for reviewable results.

Never write `AppPortal.json` or `@appconf` directly, or relay QuickConnect.
Compose has no native Application Portal alias; use its supported web entry.

Use dsm-package.yaml schema 2. Keep upstream Compose bytes unchanged; declare DSM
policy in compose.files and compose.web. Never use file/targets/address_env or
identity_gateway.upstream: the SDK planner derives ingress.

## Compose health and launch

Select compose.web.health.path and its actual expected 2xx status before
check/build. Redirects are not followed; a 302 to login is unhealthy. check is
static, not an HTTP or arbitrary-UID/storage probe. Test the selected official image as
the package UID, including writable volumes, first setup and upgrade.
Omitted ui.launch means new-page via the SDK standalone launcher, without
Application Portal. Headless Apps omit compose.web and have no launcher.
Compose ctl is unsupported.

Use supported upstream config files, environment, argv or reverse proxy for
login/settings. For integrated upstream Apps, select supported trusted-header authentication or disable upstream login behind the DSM admin gate; or use the existing SDK 0.17.3 token adapter: OpenList uses mode: token, access: dsm-admins and entry: admin-only. Its unmodified admin token CLI supplies a package-private 0600 credential; the gateway injects Authorization server-side after DSM admission, without delivering it to the browser. All DSM admins share one upstream admin; token reset requires package restart; WebDAV keeps its own credentials. Verify each App adapter and DSM admission separately.
Containers use the package account and a dedicated bridge; they do not inherit
an interactive user's NAS ACL. Do not use root/chown during any App lifecycle
phase. Preserve licenses and dependency/source provenance. Read the CLI skill
reference/compose.md and reference/upstream-fork.md for the full recipe.

Public npm access does not grant anonymous Go SDK access. Obtain authorised
source/cache access or a matching SYNOPKGLAND_SDK_DIR checkout first. Never copy
credentials into the App. Do not install, publish or modify NAS data without task authorization.
