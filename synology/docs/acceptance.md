# Release acceptance

The initial package uses the unchanged official Home Assistant 2026.10.2 image
and the pinned, unchanged hass-oidc-auth 1.2.1 component. The published
SDK/CLI/templates 0.23.0 toolchain completed check/build/inspect with no findings;
no source overrides were used. Adapter boundary tests and the owned workflow
syntax check passed.

A fresh installation on DSM 7.3.2, x86_64 with Container Manager 24.0.2 was
exercised through the DSM main menu using an IP and a separate DNS alias.
Both produced an authenticated Home Assistant administrator who was not the
bootstrap owner. An existing ordinary DSM user's verified service session
received HTTP 403 from administrator admission.

A dashboard and Markdown card were created through the UI. Native stop/start
retained the stored dashboard bytes, and the card was read back through both
origins after restart. The container ran as the package UID with
read-only root filesystem, all capabilities dropped and host networking.
Home Assistant's UDP 5353 sockets were observed; no SSDP support is claimed.

The browser test bypassed the test certificate errors. This verifies the App
flow, not certificate trust, a mobile Companion client or an upgrade.
Configure trusted DNS/TLS and the user's country/location for real use.
The initial country and migrated HTTP YAML repair prompts are upstream setup
messages. The adapter checks the promoted native loopback HTTP settings.

## Fresh-install repair fix: 2026.10.2-0011

The package now applies native location suggestions during onboarding and
removes temporary HTTP YAML before the serving restart. Offline regression
tests cover native core updates, failed detection/manual setup, configuration
preservation and loopback/proxy policy refusal. These tests are not DSM device
acceptance of the new build.

Before release, install with a fresh data volume, open Settings > Repairs and
verify both the country and HTTP YAML migration issues are absent when native
location detection succeeds. Check Settings > System > General against the
expected country, time zone and units; verify gateway entry and a native API
request through the gateway. Change the core settings, restart and confirm
they remain unchanged and both issues stay absent. With location detection
unavailable, verify startup still permits manual setup and the country issue
clears after saving a country; HTTP YAML must still be absent. Confirm the
native HTTP store binds only loopback and trusts only the loopback proxy.

Named volumes are retained by Container Manager after uninstall. See
[the data/removal limits](../README.md#data-and-removal).

Native uninstall completed. Its retained named volume and the disposable package
state were then explicitly removed; package containers, networks, runtime and
listeners were absent afterward. Container Manager stayed active.
