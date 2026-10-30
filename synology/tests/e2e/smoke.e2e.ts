import { appOpenSmoke } from '@synopackageland/cli/e2e';

// hass-oidc-auth renders this only after DSM admission and a successful native
// OIDC callback; reaching the Home Assistant UI then needs one user click.
appOpenSmoke({ ready: '#continue-on-this-device' });
