# Release notes

## 2026.10.4-0009: Installation reliability in Package Center

Rebuilt with CLI 0.53.16 to improve installation reliability in Package Center.
The ingress nginx reload is now declared only for start and stop
(`startstop_restart_services="nginx.service"`); INFO no longer declares
`instuninst_restart_services`, so installing no longer reloads nginx while DSM
is loading package information. SDK/App 0.53.25, templates 0.40.1, the upstream
version, official image and authentication policy are unchanged.

Validation: check, build, inspect comparison with 2026.10.4-0008 and leak scans.
Tests and NAS checks were not run for this rebuild.

## 2026.10.4-0008: Temporary files on disk

Temporary files move from an unbounded memory tmpfs on `/tmp` to SDK disk scratch
(`compose.services.web.scratch: [/tmp]`, with `TMPDIR=/tmp`): a package-UID-owned
mode-0700 directory on the package volume, emptied at every container start. No
memory tmpfs remains. Rebuilt with published SDK/App 0.53.25 (executor 0.53.6) and
CLI 0.52.16. The upstream version, official image and authentication policy are
unchanged. No SDK administrator approval is required; this package has no executor.

Validation: unit and entry tests, render check, check, build, inspect comparison
with 2026.10.4-0007 and leak scans. Device: upgraded from 2026.10.4-0007 on an x86_64
DSM 7.3 NAS; the container started, `/tmp` was a btrfs bind (not tmpfs) with mode
0700 owned by the package UID, writable, and the main page loaded through DSM sign-in.

## 2026.10.4-0007: Sign-in page loading reliability

Improve page loading reliability when signing in with SDK/App 0.53.21 and
CLI 0.52.13. Session admission is shared and parallel asset requests queue.
The upstream version, official image and authentication policy are unchanged.
Check, build, baseline inspect and leak scans only; tests and NAS checks were not run.
No SDK administrator approval is required; this package has no executor.

## 2026.10.4-0004: Install wizard fixes

- en-US: Install wizard: port conflicts only warn; shared folder selection fixed
- zh-TW: 安裝精靈：連接埠衝突僅顯示警告；已修正共用資料夾選擇
- zh-CN: 安装向导：端口冲突仅显示警告；已修复共享文件夹选择
- ja-JP: インストールウィザード：ポートの競合は警告のみ表示し、共有フォルダーの選択を修正
- ko-KR: 설치 마법사: 포트 충돌은 경고만 표시하고 공유 폴더 선택 수정
- de-DE: Installationsassistent: Portkonflikte zeigen nur Warnungen; Auswahl gemeinsamer Ordner korrigiert
- fr-FR: Assistant d’installation : les conflits de ports affichent un avertissement ; sélection des dossiers partagés corrigée

Built with CLI 0.47.4; SDK/App 0.42.0 and templates 0.37.0 remain pinned.
Package check, build, inspect and leak scan only; no tests or NAS checks were run.
Approval retention is unknown; administrator approval may be required after upgrading.

## 2026.10.4-0003

Built with published SDK/App 0.42.0, templates 0.37.0, CLI 0.42.2 and executor
v0.39.0. Home Assistant 2026.10.4 and its official image are unchanged. The DSM
entry remains `/webman/3rdparty/SynoPkgHomeAssistant/sso/open.cgi`, opening the
gateway on its dedicated origin. Native daemon ingress at
`/synopkgland/SynoPkgHomeAssistant/` is unsupported for this Compose package;
administrator-only entry and native-client authentication policy are unchanged.

Approval retention is unknown. The current CLI rejects the previous published
SPK as an invalid baseline (`COMPOSE_ARTIFACT_INVALID`); administrator approval
may be required after upgrading. One existing installation passed an in-place
upgrade from 2026.10.4-0002: running, administrator DSM launch and core settings
retention were verified. The native daemon ingress URL returned HTTP 404.
Full E2E and broader lifecycle/device acceptance were not run.

## 2026.10.4-0002

Built with published SDK/App 0.38.2, templates 0.35.5, CLI 0.41.9 and executor
v0.38.2. The install wizard now selects the gateway HTTPS and OIDC issuer ports;
upgrades keep the defaults 8125 and 8126. Entry and login policy are unchanged:
DSM administrators only. Protected executors require administrator approval.

## 2026.10.2-0010

Built with published SDK/App/templates 0.32.0, CLI 0.34.0 and executor v0.32.0.
The fixed client prefixes in the README use upstream authentication; browser
entry and every unlisted route retain the existing DSM gate. Entry and login
policy are unchanged. Protected executors require administrator approval.
Mobile/native first-login and deployed client acceptance remain unverified.
See [mobile and native clients](../README.md#mobile-and-native-clients) for the
exact prefix list, upstream credentials, revocation and client limitations.
