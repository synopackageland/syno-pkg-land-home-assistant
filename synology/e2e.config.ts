import { dsmTarget } from '@synopackageland/cli/e2e';

export default {
  tests: ['tests/e2e/**/*.e2e.ts'], targets: [dsmTarget()], workers: 1, retries: 0,
  output: process.env.DSM_E2E_OUTPUT_DIR ?? '.e2e/output',
};
