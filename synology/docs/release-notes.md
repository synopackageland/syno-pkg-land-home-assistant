# Release notes

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
