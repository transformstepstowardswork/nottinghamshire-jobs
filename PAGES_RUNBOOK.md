# Verified Pages commissioning and recovery

This is preparation, not permission to activate. ANT-425 Tier 1 produces a
non-main review candidate. Anthony controls each setting/permission change,
exact main merge and real deployment/CMS write. Independent technical/security
review of the final publisher and this sequence is required before promotion.

## Source and live checkpoint — 10 November 2026

- Repository: `transformstepstowardswork/nottinghamshire-jobs`.
- Live-source reference: `main` = `a1398beaae7865627f6c323d9d8bb71e73670509`.
- Accepted stacked source: ANT-423 `037bfdeb2c0c66a96fd1f94c70c4de1fed2c982c`
  → ANT-424 `93fa3cd0faaf97d564da02891f5121da9d69c88c` → ANT-425 review branch
  `codex/ant-425-verified-pages-commissioning`. Final review SHA/evidence is in ANT-425.
- Root, `/support.html` and `/jobs.csv` returned HTTP 200. The public CSV matched
  source: 446 rows, 16 columns, SHA-256
  `1560694e55c22891380df0d4bd8385975b8ed2e10fa139e4694f0422fbaa625a`.
  Support retained `https://forms.cloud.microsoft/e/7A0mceck5C`.
- Protected Git blobs: `app.js` = `4f81cb3c499c6ea45ad3e4de7e44fb66e4e2129b`;
  `jobs.csv` = `ca4759693da9d9c98a9b7c9d34f402e31fd4b0fb`.
- Historical Pages run `42603046472` has successful internal Jekyll build and
  deploy jobs. Current source/operational reports indicate branch-source
  publishing from main root. The connector cannot read the actual Pages Source
  setting, active environment rules or CMS App installation. Repository metadata
  reports admin/maintain/push for the connected Transform account; the actual
  owner's commissioning-session access and settings are still **unverified**.

Recheck all refs, public feed bytes, outstanding PRs/runs and settings at the
actual gate. Weekly Jobs updates may advance main. Never replace newer Jobs
data with this snapshot. Preserve the public provider URL:
`https://transformstepstowardswork.github.io/nottinghamshire-jobs/jobs.csv`.

## What the source candidate enforces

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

## Owner-controlled activation, in order

1. Obtain genuinely independent review PASS for the exact final candidate and
   approval sequence. Anthony supplies/approves substantive Traditional Chinese
   Support text before full bilingual release; agents must not invent it.
   The accepted Chinese-interface/English-body interim is not that content PASS.
   An interim public launch requires Anthony's explicit changed product decision.
2. In an authorised owner session inspect current Pages Source, repository
   admin/maintainer rights, Actions policy and `github-pages` environment. Record
   the exact current main SHA, latest deployed run/SHA and public feed checksum.
   Inspect outstanding runs and competing deploy workflows. Stop on conflict.
   Prepare environment branch restrictions for main only, with any permission or
   protection changes separately approved. Do not expand repository/App access.
3. Prepare the reviewed combined source on the non-main branch. If main advanced,
   reconcile its changes conservatively there, preserving the latest `jobs.csv`
   and manual weekly controls. Record old main, reviewed candidate and reconciled
   candidate SHAs/diff; refresh affected CI/review. Do not promote ANT-423 alone.
4. **With explicit Pages-setting approval, change Settings → Pages → Source from
   Deploy from a branch to GitHub Actions BEFORE merging any editorial source.**
   Skip GitHub's suggested starter workflow: it would omit the verifier. Record
   the actual selected mode and check no old branch-source deployment remains
   queued/in progress before promotion. Do not merge if the change cannot be
   confirmed or another publisher can still bypass the gate.
5. **With separate exact source-SHA/target/merge-method and production-activation
   approval**, promote the single reviewed combined candidate to main. This push
   activates `Publish verified Pages`, so merge approval must explicitly include
   that production consequence. Record the resulting main SHA (it may differ
   after merge), build/run IDs, verifier PASS, artifact ID and deploy outcome.
   Stop on failure before any further mutation. Do not manually invoke a default
   Pages workflow, bypass a verifier or switch back to branch publishing.
6. Freshly verify root, Support, four navigation routes, `?lang=zh-Hant`, both
   language archives/details, images/alt, tags, event-time boundaries and compact/
   keyboard reading. Check the exact public CSV bytes/row count with cache bypass,
   My Next Step provider URL and Forms destination. Record observed deployed SHA.
7. Only after separately authorised repo-only hosted Pages CMS App installation/
   permission and editor enablement, perform Anthony's real authoring UAT. Inspect
   requested scopes and limit installation to this repository. `.pages.yml`
   exposes only four editorial collections and repository images, but is **not**
   a repository-path ACL for the GitHub App. Current scopes/access remain unknown.
   Test independent English and zh-Hant Article and Activity create/edit/delete,
   approximately 1,000-word Activity rich text, repeatable Article topics, cover
   and inline images with alt, stable URLs and Git commits. Use approved public
   content or an owner-approved non-main CMS branch if supported. No fictitious
   public listings or sensitive test content. Observe verified publication after
   Save, then Anthony's integrated UAT and separate final release acceptance.

GitHub documents selecting Actions without first installing a workflow on main;
no bootstrap main commit is currently indicated. Source-mode switching may leave
the current site available, but continuous service and last-good retention have
not been tested here. Allow a short owner-agreed maintenance window between mode
switch and first verified deployment. If the UI requires a bootstrap or settings
behave differently, stop and shape an exact minimal file set and additional
owner-controlled merge gate; do not create an unverified starter publisher.

## Failure, rollback and weekly operation

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
- **Recovery after a successful guarded deployment:** record that known-good
  deployed combined SHA and public CSV checksum. Prepare a non-main recovery PR
  reverting only the faulty editorial/content or source change to the last good
  verified version, retaining the publisher, verifier and latest approved Jobs
  feed. Run relevant gates, review and obtain Anthony's exact merge/deployment
  approval. Let the same pipeline rebuild, verify and deploy; smoke the result.
  Never revert all of main to the old pre-Actions snapshot, delete the verifier/
  publisher, or restore unsafe branch-source publishing.
- **First handover fails before any good Actions deployment:** the old main SHA
  above identifies the previous live assets/feed, not a ready guarded rollback
  commit. Preserve those assets/data while preparing a reviewed repair on the
  combined branch and obtaining specific promotion/deploy approval. If necessary,
  remove faulty new editorial records in that repair while keeping archive shells
  and all safety gates. A site outage is possible until the guarded repair works.
  Restoring a previously uploaded artifact is not a tested recovery path here;
  readiness artifacts expire after 3 days and are not deployment authority.
- **Routine Jobs:** continue `job-update/YYYY-MM-DD`, a `jobs.csv`-only PR, existing
  validation and Anthony's squash merge. After commissioning, that approved main
  push automatically attempts the same verified production build. Confirm public
  feed bytes before declaring the weekly update online. CMS does not manage Jobs.

## Platform references

- [Custom Pages workflow, artifact format, permissions and job dependency](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- [Publishing source selection, existing workflows and environment restrictions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [Official Jekyll builder inputs](https://github.com/actions/jekyll-build-pages/blob/v1/action.yml)
- [Official Pages artifact uploader](https://github.com/actions/upload-pages-artifact/blob/v4/action.yml)
- [Pages CMS configuration](https://pagescms.org/docs/configuration/) and [rich-text field](https://pagescms.org/docs/configuration/fields/rich-text/)
