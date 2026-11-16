# Verified Pages publishing and recovery

This runbook covers the established GitHub Actions publisher for
`transformstepstowardswork/nottinghamshire-jobs`. Routine Jobs, Article and
Activity updates use this existing publication path. Initial commissioning is
complete; the original activation checklist and pre-launch snapshots remain in
Git history, not as outstanding requirements for ordinary content updates.

Anthony retains merge/publication authority. Changes to the publisher, Pages
settings, environment rules or CMS App access require their own applicable
review and approval; routine content editing does not authorise those changes.

## Routine content publication

1. Prepare the approved change against current source. Use the
   [editor guide](EDITOR_GUIDE.md) for Articles and Activities and the
   [weekly update instructions](README.md#weekly-update) for Jobs.
   Preserve unrelated content and the latest approved `jobs.csv`.
2. Check the exact candidate using the relevant PR validation. For editorial
   changes, `Verify Pages readiness` builds and verifies real output without
   deploying. An unchanged candidate can reuse its valid check/review evidence.
3. Obtain the applicable approval for the exact change reaching `main`.
   CMS Save creates a Git commit; when saved on the publishing branch it can
   trigger publication. Saving on a non-main branch does not itself deploy.
4. Follow `Publish verified Pages` for the actual resulting `main` SHA, which
   may differ from the reviewed PR head after merging. Confirm build, output
   verification, artifact upload and deployment success. A green PR, saved
   commit or successful merge alone does not establish live publication.
5. Open the affected public entry and its language archive, check its image
   and links, and retain the observed run/revision and remaining limitations.
   For Jobs, verify the public CSV's row count and checksum against the approved
   candidate. Record Anthony's visual confirmation separately from automated
   endpoint checks.

Inspect current workflow/run evidence when diagnosing publication. An old draft
commissioning PR or historical uncertainty about settings is not evidence that
the current publisher needs activation again. Do not switch to branch-source
publishing or install a starter workflow to bypass the verifier.

Keep documentation/source cleanup separate from normal `jobs.csv`-only PRs.
Every approved main push, including a documentation-only merge, triggers the
publisher. Such a merge rebuilds with the existing Jobs feed; it is not a fresh
weekly vacancy update. Preserve the public provider URL:
`https://transformstepstowardswork.github.io/nottinghamshire-jobs/jobs.csv`.

## What the publisher enforces

`pages-publish.yml` runs only on a push to main. It checks out the triggering
immutable SHA with no persisted Git credential. The shared
`build-verified-pages` action builds once with the Pages-compatible Jekyll
builder (`_config.yml` retains `/nottinghamshire-jobs`), verifies real editorial
HTML, then checks public entry points, archives, byte-identical source assets,
local resource URLs, Forms destination and the existing CSV safety contract.
Only success uploads that same `_site` through `upload-pages-artifact@v4`.
The downstream deploy job needs successful build, uses `github-pages`, and has
only `pages: write` and `id-token: write`. It never checks out or rebuilds content.

Build/CI tokens have only `contents: read`. No new secret or admin token is
needed. `configure-pages` is unnecessary here: the accepted Jekyll configuration
already supplies the fixed base path; the proven source-only builder needs no
account-setting action. The workflow never enables Pages itself.

Production concurrency cancels superseded runs; a public main-ref check before
deploy refuses stale reruns. Cancellation/ref checks reduce ordering risk but
are not an atomic lock on the external Pages service. Observe the final deployed
SHA; do not claim an in-flight provider deployment can always be cancelled.
There is one deploy workflow and no manual, PR, preview or fixture deploy route.

`pages-readiness.yml` packages real output with the official Pages uploader under
the distinct `pages-readiness` name. A downstream read-only job downloads it,
checks the exact tar SHA-256, extracts and rechecks it. A separate hostile fixture
job exercises the same production gate and requires rejection of generated
unsafe HTML plus skipped upload. `jekyll-source-spike.yml` retains the safe
language/tag/lifecycle fixtures and deliberate negative build. Its ordinary
test artifacts are never production inputs. These checks do **not** deploy,
test actual Pages settings or prove last-good-site retention.

## Publisher and CMS access changes

For an authorised publisher/settings/access change, inspect the actual current
Pages Source, Actions policy, competing deployment routes, `github-pages`
environment and account/App permissions relevant to that change. Resolve a
concrete conflict before the dependent action; do not infer current state from
a historical snapshot or failed request to an incorrect repository.

Use the applicable technical/security review and Anthony's specific approval
for the changed mechanism or permissions. Keep the guarded Actions publisher,
main-only deployment and minimum permissions; do not expand App access as a
side effect of editorial work. The CMS configuration exposes four collections
and repository images but is not a repository-path ACL for the GitHub App.

Use approved public content for any authorised CMS tests. Repository content,
including committed drafts, is public and must not contain participant-private
information. Test only the affected authoring capabilities; do not claim that
all languages, create/edit/delete operations or image flows were tested from
one successful entry.

## Failure and recovery

- **CMS Save succeeds but verification fails:** the Git commit exists; new content
  is not published by this pipeline. Check the failed run for that commit. Remove
  the indicated unsafe link/unsupported HTML or fix the missing image/alt, then
  Save and observe a new verified build. Do not equate Save with publication.
  The pipeline makes no deploy request on gate failure; continued availability of
  the previous site is expected but must be observed, not promised.
- **Build/upload fails:** no downstream deploy. Preserve the error/run/SHA, repair
  the source or infrastructure cause and verify the changed candidate. A stale
  run refusal means newer main must be assessed; never rerun an old commit to
  overwrite newer content. An exact-current rerun reuses the guarded pipeline;
  any real deployment still requires the applicable owner authority.
- **Deploy fails or site is wrong:** inspect actual Pages run/environment and live
  endpoints before another action. Provider failures may affect availability.
  Do not assert rollback happened because an Action failed.
- **Recovery after a successful guarded deployment:** record the known-good
  deployed SHA and public CSV checksum. Prepare a non-main recovery PR
  reverting only the faulty editorial/content or source change to the last good
  verified version, retaining the publisher, verifier and latest approved Jobs
  feed. Run relevant gates, review and obtain Anthony's exact merge/deployment
  approval. Let the same pipeline rebuild, verify and deploy; smoke the result.
  Never revert all of main to a pre-Actions snapshot, delete the verifier/
  publisher, or restore unsafe branch-source publishing.
- **Artifact recovery:** restoring a previously uploaded artifact is not a
  tested recovery path. Readiness artifacts expire after 3 days and are not
  deployment authority; use the reviewed repair and guarded publication path.

## Weekly Jobs updates

Continue the [normal weekly workflow](README.md#weekly-update): a dated branch,
normally `job-update/YYYY-MM-DD`, a `jobs.csv`-only PR, existing dataset
validation and Anthony's approved squash merge. The current weekly Skill and
Playbook own collection, judgement and candidate preparation. Do not add
documentation, editorial content or publisher changes to a routine Jobs PR.

The approved main push automatically attempts the same verified production
build. Confirm the deployed main revision and public feed bytes, row count and
checksum before declaring the weekly update online. The public-site verifier
requires the built `jobs.csv` to match the checked-out source byte for byte and
pass the existing CSV safety contract. CMS does not manage Jobs.

## Platform references

- [Custom Pages workflow, artifact format, permissions and job dependency](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- [Publishing source selection, existing workflows and environment restrictions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [Official Jekyll builder inputs](https://github.com/actions/jekyll-build-pages/blob/v1/action.yml)
- [Official Pages artifact uploader](https://github.com/actions/upload-pages-artifact/blob/v4/action.yml)
- [Pages CMS configuration](https://pagescms.org/docs/configuration/) and [rich-text field](https://pagescms.org/docs/configuration/fields/rich-text/)
