# Changelog

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

## 2026.10.4-0003: CLI 0.42.2 rebuild

Built with SDK/App 0.42.0, templates 0.37.0, CLI 0.42.2 and executor v0.39.0;
Home Assistant 2026.10.4, the official image and the administrator-only policy
are unchanged. The generated DSM launcher retains its Compose gateway entry;
the native daemon ingress path does not apply to this Compose package.

Approval retention is unknown: the previous released SPK is not a valid
baseline for this CLI. Administrator approval may be required after upgrading.

## 2026.10.4-0002: SDK 0.38.2 rebuild

Built with SDK/App 0.38.2, templates 0.35.5, CLI 0.41.9 and executor v0.38.2;
Home Assistant 2026.10.4 and its official image are unchanged.

- The install wizard selects the gateway HTTPS and OIDC issuer ports
  (defaults 8125 and 8126); the adapter follows the selected issuer port.
- Add the app-open smoke (`npm run e2e:smoke`) for administrator, normal-user
  denial and signed-out access.

## 2026.10.2-0011: Fresh-install Repairs

- Save native country, time zone and unit suggestions during first onboarding;
  request manual setup if location detection is unavailable.
- Remove temporary HTTP YAML before the serving restart and retain the native
  loopback listener and trusted-proxy configuration.
- Add bootstrap regression checks; DSM acceptance remains a release gate.


## 2026.10.2-0009: SDK entry-gate migration

Built with SDK/App/templates 0.32.0, CLI 0.34.0 and executor v0.32.0.
Every request retains the DSM entry gate. No upstream-authenticated path exceptions are enabled in this build.
Protected executor payloads changed: administrator approval is required again after upgrading.
No NAS installation or device acceptance was performed for this rebuild.

## 2026.10.2-0006

- Improve opening the App from the DSM menu and external access settings
- 改善從 DSM 選單開啟 App 與外網存取設定
