---
name: nottinghamshire-editorial
description: Create or edit Nottinghamshire Jobs / Transform Training Articles and Activities from supplied notes, flyers, text, images or source links, in English and/or Traditional Chinese. Use only in the transformstepstowardswork/nottinghamshire-jobs repository. Excludes weekly vacancy updates and website/CMS development.
---

# Nottinghamshire Articles and Activities

Turn Anthony's material into accurate, readable entries using the same content
files as Pages CMS. This is an editorial workflow, not a new CMS integration.

## Establish scope and current sources

- Follow the repository `AGENTS.md`, including its linked J_OS entry when
  applicable; reuse instructions already read. Verify the working repository is
  `transformstepstowardswork/nottinghamshire-jobs` and inspect branch/status
  before edits. If the repository identity differs, stop repository writes.
- Read [the editor guide](../../../EDITOR_GUIDE.md) and
  [the CMS schema](../../../.pages.yml) for every new task, reusing current reads
  within a continuing task. They own field meanings and storage. Inspect the
  target entry before editing it.
- Establish whether the request is for an Article or Activity, new content or an
  edit, and which language(s). Infer clear choices from the request/material.
  Ask only about ambiguity that changes the result; continue drafting anything
  that does not depend on the answer.
- Match the requested endpoint: chat draft, local content files, or authorised
  publication. A request to draft or create content does not itself authorise
  committing, pushing, merging, CMS Save or deployment. Honour authority already
  granted; do not ask for it again.

## Prepare the copy

Use the supplied material as factual evidence. Read supplied source links when
needed to support the entry; do not present an unread link as verified. When
sources conflict, resolve with Anthony rather than inventing the consequential
fact. Do not expand a simple drafting request into unrelated research.

Write clear, welcoming copy for Transform's public readers. Preserve the
author's meaning and requested voice; retain supplied final wording unless an
edit is requested. A title and concise summary should help readers understand
the entry. Use headings, paragraphs and lists when useful, without forcing
every entry into a fixed outline.

Never invent dates, cost, eligibility, services, outcomes or registration links.
Keep unknown optional fields absent or blank, letting the site's existing
fallbacks explain them. Ask for a missing required fact, such as an Article's
publication date, while preparing the remaining draft. Do not silently use the
file-creation date as the publication date.

English and Traditional Chinese are independent collections. Create or translate
both only when requested; otherwise use the intended language. Preserve names,
addresses, links and factual meaning across requested translations. Do not put
confidential participant information into public content or committed drafts.

## Post structure

The layouts supply the page heading and metadata; do not repeat the title as
a Markdown H1 or paste metadata into the body as a second details panel.
Use [the entry layout](../../../_layouts/editorial.html) and
[the archive card](../../../_includes/editorial-card.html) for current rendering.

| Part | Article | Activity |
| --- | --- | --- |
| Heading and metadata | Title, publication date, optional category | Title |
| Introduction | Short summary | Short summary |
| Topics and image | Relevant article tags, then optional described cover | Optional described cover |
| Structured details | No event details panel | Dates/times, venue, organiser, eligibility, cost, then registration/details link |
| Main Markdown body | Opening/context, useful detail, and a next step or source link where relevant | What the activity involves, what to expect, and any supplied preparation or attendance instructions |

These are content relationships, not compulsory prose headings. Adapt the body
to the material, preserve supplied final copy, and avoid padding a short entry.
Keep metadata and body facts consistent; do not duplicate the summary verbatim.
In a chat draft, present the intended metadata and body clearly so Anthony can
review both before files are written or published.

## Reuse article topics

Before choosing tags for a new or edited Article, inspect the existing
`tags` frontmatter in the target language's article collection. Read actual
YAML values, including inline lists if present, rather than guessing a taxonomy.
Consult the other language's collection when helpful for established names,
but prefer labels already used in the target collection. There is no separate
hand-maintained tag registry.

Add a small set of useful, relevant tags where they help readers find related
articles. Reuse an existing matching label with its established spelling and
capitalisation. Avoid near-duplicate synonyms, translated variants of an
established programme name, and case/spacing variants. Preserve unrelated
existing tags on edits. A category does not replace the article's topic list.

Introduce a concise new tag only when the subject is useful to filter by and
no existing tag fits; do not invent a new label for every post or attach an
irrelevant existing tag just to reuse it. If no topic is useful, leave tags
empty. Deduplicate the final YAML list and omit leading `#`. Do not add article
tags to Activities: the current Activity schema has no topic field.

## Write CMS-compatible files

Use [the CMS schema](../../../.pages.yml) as the current field authority and
[the site configuration](../../../_config.yml) for collection defaults and URLs.

| Entry | English | Traditional Chinese |
| --- | --- | --- |
| Article | `_articles_en/` | `_articles_zh/` |
| Activity | `_activities_en/` | `_activities_zh/` |

Write UTF-8 Markdown with YAML frontmatter. Put the main content after the
closing `---`; the CMS's `body` field represents that Markdown, not a separate
frontmatter string. Quote YAML strings where necessary so colons, quotes, dates
and line breaks retain their intended values.

- Articles currently require `title` and `date` (`YYYY-MM-DD`). Optional fields
  include `summary`, `category`, `tags`, `image` and `image_alt`. Store topics
  as a YAML list without leading `#`.
- Activities currently require `title`. Use available `summary`, `start_date`,
  `start_time`, `end_date`, `end_time`, `venue`, `organiser`, `eligibility`,
  `cost`, `registration_url`, `image` and `image_alt`. Dates use
  `YYYY-MM-DD`; times use quoted 24-hour `HH:MM` in Europe/London. Check
  supplied dates/times agree with the text. Unknown cost does not mean free.
- New entries use an unused timestamp filename following the CMS template
  `YYYY-MM-DD-HH-MM-SS.md`. Check for collisions before writing. For an edit,
  preserve its filename, URL, unrelated fields and content even if the title
  changes. If the requested existing entry is ambiguous, clarify its identity.
- Use provided images or approved existing repository images. Store new media
  under the configured `media/images` location; public image paths currently
  begin `/nottinghamshire-jobs/media/images/`. Add meaningful alt text to cover
  and inline images. Do not reference a local computer path or remote image as
  though it were a repository image.
- Prefer ordinary Markdown. Avoid embedded forms, iframes, scripts, raw HTML
  comments and unsupported markup. Registration URLs must be HTTP(S); internal
  links must respect the site's base path. The generated-HTML verifier owns the
  exact allowed markup and URL policy.

Limit edits to the requested entries and their media. Do not alter `jobs.csv`,
site code, CMS configuration or publishing workflows as part of this skill.
When a request needs those changes, surface that separate scope.

## Check and present the result

For a chat draft, show the content and any unresolved factual questions; no
repository build is needed.

For local files, inspect the actual diff and new files. Check YAML parses,
required fields, collection/language, body placement, factual consistency,
dates/times, topics, links and image paths/alt text. Check that unrelated work
is preserved. Do not add an invented `draft` flag: these collections currently
have no configured private draft workflow. Local uncommitted files are not
automatically available in the hosted CMS.

Before claiming a publishable build, use real Jekyll output and the existing
checks, run from the repository root:

```powershell
py -X utf8 scripts/verify_editorial_html.py _site
py -X utf8 scripts/verify_public_site.py _site
```

The existing build recipe is
[build-verified-pages](../../../.github/actions/build-verified-pages/action.yml).
A plain static server, Markdown preview, fixture output or a stale `_site`
directory is not proof that the candidate builds. If a real local Jekyll build
is unavailable, report that limit; do not install a new toolchain just for a
routine entry. The existing non-deploying
[Pages readiness workflow](../../../.github/workflows/pages-readiness.yml)
can verify an authorised remote candidate. Passing unit tests alone does not
verify generated pages.

Return the readable draft or changed file links, requested language(s), missing
facts and checks actually performed. Distinguish a chat draft, local files,
remote saved content and a verified live page. Stop at the requested endpoint.

## Publication only when authorised

Follow current J_OS change-control/release authority where applicable. Read
[the publishing runbook](../../../PAGES_RUNBOOK.md) and
[the current workflow](../../../.github/workflows/pages-publish.yml) for the
action in scope. Use the established publisher for routine editorial updates;
do not repeat initial commissioning. Inspect current workflow/run evidence for
a publication failure and surface a real current conflict if one exists. Changes
to the publisher, Pages settings or CMS permissions are separate from routine
content editing and require their own applicable review and approval.

### Keep repository and PR identity consistent

Use the read-only [publication context helper](scripts/publication_context.py)
from this repository before GitHub PR operations. With no arguments it verifies
origin against this project and emits the repository identity to reuse for PR
creation. For an existing PR, supply its actual URL from Anthony or a successful
GitHub response to obtain consistent connector arguments and URLs:

```powershell
py -X utf8 .agents/skills/nottinghamshire-editorial/scripts/publication_context.py --pr-url PR_URL
```

Parse its JSON and reuse `read_pr_args` directly, adding the selected connector
`link_id`. Once a merge is authorised, rerun with `--expected-head` set to the
full reviewed PR head SHA and `--merge-method` set to the agreed method. Reuse
`merge_pr_args` directly with `link_id`; do not retype the repository owner
between reads, permission checks, merges and reported links. Validate the live
PR's base repository, target branch and head against the authorised candidate
before merging. The helper constructs arguments; it does not verify live
checks, choose an account, grant authority or perform publication.

Copy returned canonical URLs for reports. If Anthony corrects an identifier,
use the correction and verify it against origin/the successful response; do not
revert to an earlier assistant-written link or ask for the same known value.

### Recover from a failed GitHub call

Before retrying or diagnosing access, compare the actual failed tool arguments
with the verified repository, PR number, selected account and expected head.
A 404 alone does not establish a missing PR, broken connection or insufficient
permission. If the request differs, rebuild it from the checked context and
continue within existing authority. Do not recreate a PR, switch accounts or
request reconnection to work around a misspelled repository.

When the correctly addressed request still fails, inspect the exact error and
the tool's supported endpoints. Use the appropriate PR/run/job tools; a
PR-triggered-only workflow lookup cannot establish that a push deployment is
absent. An unsupported endpoint does not prove a GitHub outage. Use a supported
read-only route where available. After an ambiguous mutation result, read
current PR/merge state before attempting the action again. Stop dependent work
only for a genuine unresolved access, identity, candidate or authority boundary;
report the observed limitation without inventing its cause. Preserve previous
valid checks and approval when the candidate and action are unchanged.

### Verify completion

Reuse the existing verified publisher. CMS Save creates a Git commit and can
trigger publication; it is not merely a local draft save. A successful merge
or green PR checks do not prove deployment. Follow the production run for the
actual merge/main revision, confirm build and deploy success, then check the
public entry, language-specific archive, image and registration link.

If the run is pending, continue bounded checking in the current chat within
the task rather than ending with an unchanged status or asking Anthony to
repeat authorisation. On a genuine failure, capture the exact error, preserve
the gate and distinguish saved, merged and deployed state. Record Anthony's
visual confirmation separately from automated checks; do not claim a visual
check merely from HTTP 200.