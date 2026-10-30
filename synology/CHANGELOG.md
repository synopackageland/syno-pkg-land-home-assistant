# Changelog

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
