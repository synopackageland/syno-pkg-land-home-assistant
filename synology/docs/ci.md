# Package CI and upstream upgrades

Our only allowed workflow is `.github/workflows/synopkgland-synology-fast-ci.yml`.
Upstream files, including their workflow names and content, remain unchanged.
Package checks use GitHub-hosted `ubuntu-latest`, ordinary `pull_request` events,
read-only repository permissions and no secrets.

Fast package checks validate the rendered Compose adapter and nonroot/listener refusal tests without private SDK credentials. Workflow/docs-only diffs validate our
workflow syntax but skip product checks; green CI is not release certification.
Full matrices, package/runtime acceptance and publication remain release gates.

## Initial activation after this PR merges

Use the trusted SDK checkout's `ops/private-ci/workflow-policy.py` on the
operator's computer. Use a mode-0600 token file; never put a PAT in argv or in
this repository. The operator token needs Actions write, Administration write,
Contents read and Metadata read for this repository. It is separate from the
private runner's runtime token and must never enter a job.

1. Keep repository Actions disabled while merging this PR. Do not push or open
   another PR during activation; finish or cancel any unfinished runs first.
2. From the trusted SDK checkout, run (replace `/secure/operator-token`):

```sh
python3 ops/private-ci/workflow-policy.py synopackageland/syno-pkg-land-home-assistant \
  --token-file /secure/operator-token --mode activate
```

3. The script first checks queued/in-progress/waiting/requested/pending runs,
   sets public fork PR approval to `all_external_contributors`, and disables
   every workflow except our exact path **while repository Actions is off**.
   It checks the default-branch file inventory and workflow registry, enables
   only our workflow, then enables repository Actions and reads everything back.
   Any failure leaves repository Actions off. Readback must show only our path
   as `active`; every inherited file workflow must be `disabled_manually`.
4. GitHub-managed `dynamic/dependabot/dependabot-updates` is the sole dynamic
   exception. It is not an inherited file workflow and remains separately
   inventoried. Every inherited file workflow stays disabled; the maintenance
   script fails closed if it cannot verify the exact owned path.

## Every upstream tag upgrade (required)

Before the existing upgrade/build procedure merges an upstream tag, pause CI:

```sh
python3 ops/private-ci/workflow-policy.py synopackageland/syno-pkg-land-home-assistant \
  --token-file /secure/operator-token --mode pause
```

Drain unfinished runs. Merge the upstream tag using the normal upgrade procedure;
keep upstream files unchanged. New upstream workflows may become registered as
active, so rerun `--mode activate` above **after every tag merge**, before any
further push/PR activity. Do not enable Actions by hand first. Read back the
single active owned workflow and the public fork PR approval policy. If the API
has not indexed new files yet, leave Actions off and retry once it has.

`--mode prepare` performs the disabling/readback without enabling Actions and
works even before our workflow is merged. It is safe to repeat. The workflow
never has the maintenance token and never changes repository settings itself.
