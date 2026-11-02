# Release notes

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
