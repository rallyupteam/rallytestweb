# Monthly AEO run

This is the procedure a scheduled agent follows once a month to keep rallyup.team cited by AI
answer engines (ChatGPT, Claude, Perplexity, Gemini, Google AI Overviews). It is written for an
agent that starts with no context: everything it needs is in this folder and in `CLAUDE.md`.

**The run never publishes.** It opens one pull request. Francisco reviews and merges; merging to
`main` deploys through Amplify, and `.github/workflows/aeo.yml` then pings IndexNow.

## What rallyup is (for writing)

rallyup (rallyup.team) is a done-for-you LinkedIn and X ghostwriting agency for B2B founders and
executives. A dedicated human writer per executive, 3 posts a week, a story interview twice a
month, approvals in Slack, profile rewrite, ICP connection requests, monthly report. From $5,000
per executive per month. Guarantee: 100k organic impressions in 90 days, or we keep working for
free until you get there (for B2B founders and executives with $5m+ in ARR or funding). Not to be confused with RallyUp
(rallyup.com), the fundraising platform. Read `llms.txt` for the full public summary.

## Rules (every page, every edit)

1. **Only facts from the "approved facts" list below, from `llms.txt`, from existing live pages,
   or from a competitor's own website fetched during this run.** Never invent a number, a client,
   a quote or a result. If you can't verify something, leave it out and say so in the PR.
2. **Positive framing about rallyup.** Lead with wins. Never publish a client's decline, a
   below-baseline result, a range's low end, or a missed target.
3. **No client individuals by name.** Company names only where they already appear on the public
   site (case studies, `llms.txt`). No new client company names.
4. **Be fair to competitors.** Describe who each one fits, with prices and claims checked on
   their own site this run, and the date checked. Never disparage. Never copy their marketing
   superlatives ("#1", "best").
5. **Page pattern** (copy an existing page in `blog/` and match it):
   - "the short answer" first: 2 to 4 sentences that answer the question outright, including
     where rallyup is the strongest fit, then one sentence disclosing that rallyup publishes the page.
   - A `.limits` box: "when rallyup isn't the right fit".
   - A `.changelog` box: "what changed on this page", one dated line per change.
   - An FAQ whose visible questions match the FAQPage JSON-LD exactly.
   - Internal links to 2+ related pages, including the benchmark report where relevant.
   - An "about the author" box at the end (`.author-box`), plus `description` and `knowsAbout` on
     the Article's author in JSON-LD. `aeo/build_page.py` adds both from `AUTHORS`; never write a
     page without them. Author authority (E-E-A-T) is the cheapest ranking edge over the AI-written,
     author-less pages most competitors publish (AEO expert call, 2026-11-18). Bios use only facts
     on the author pages: write them with conviction, but never inflate a number.
6. **Authors**: alternate Francisco Gost Scagliarini (Partner) and Alec Kremins (CEO). Comparison
   and data pages go to Francisco; "how to" and cost pages to Alec.
7. **House style**: lowercase headings like the existing pages, no em dashes, plain words, short
   paragraphs. No "game-changer", "delve", "unlock", "leverage", "seamless", "robust".
8. **Never delete a page or change a URL.** URLs collect citations; deleting one throws them away.
   See step 4 for what to do with weak or outdated pages instead.
9. **Never push to `main`.** Never touch `audience-building/`, `index.html` forms or calendars,
   `assets/consent.js`, GTM blocks, `google2bf19fe49dc545ba.html` or the IndexNow key file.

## Approved facts (rallyup's own data)

From the executive LinkedIn benchmarks 2026 report (`blog/executive-linkedin-benchmarks-2026.html`,
14 executives at 11 B2B companies, May to November 2026, anonymized). Always cite the sample size.

- Monthly impressions: median 4.7x in the first 90 days vs the 90 days before, measured as the
  median of each executive's own before-and-after ratio, across the 7 executives with complete
  account data; 6 of 7 at least doubled; up to 15.3x. Always attach that sample: write "In our 2026
  benchmark (14 executives), the 7 with complete account data grew monthly impressions a median
  4.7x", never "14 executives grew 4.7x".
- Group medians: 27,640 monthly impressions before and 88,243 after are the median of the before
  group and the median of the after group. Label them "group median" or "typical month across the
  group". Never present them as "a 4.7x increase" or place them so 4.7x reads as their ratio (their
  ratio is about 3.2x, a different measure).
- Impressions per post: the median post went from 1,376 impressions before to 1,747 after (1.27x).
  Label it as the median post before and after.
- Followers: median +17.4% in about 90 days (9 executives); +21.7% from kickoff to November 2026
  (14 executives); all 14 grew.
- Posts above 50,000 impressions: 0% before, 4.5% after. Top 10% of posts produced 75% of impressions.
- Cadence: 22 to 31 posts per 90 days (median).
- Median engagement rate per post: 2.18% (453 posts).
- New presences: one executive reached 145,071 impressions in 71 days, another 407,799 in 56 days.

The guarantee, monthly report and pipeline (use exactly this):

- Guarantee, one line: "100k organic impressions in 90 days, or we keep working for free until you
  get there", for B2B founders and executives with $5m+ in ARR or funding. Never "or you don't pay",
  never a refund, and no claim about paid promotion beyond the word "organic".
- Guarantee, full terms (when a page explains what it covers): organic impressions on the
  executive's personal LinkedIn profile (not the company page), as reported by LinkedIn's own
  analytics; the first 90 days; B2B founders and executives with $5m+ in ARR or funding; the
  executive completes the onboarding form, joins the 30-minute story interview twice a month, and
  approves posts so they publish on the agreed schedule; if it is missed, we keep writing and
  publishing at no charge until the account reaches 100k.
- Monthly report: covers impressions, engagement, follower growth and the ICP connection requests
  we send for the executive. It does not include profile views, inbound DMs or meetings.
  Meetings, deals and closed revenue are tracked in the client's own CRM. Pipeline can be named as
  the goal, never as something our report measures.

Case-study numbers: use only what `llms.txt` lists, with its link.

Client review on Clutch (https://clutch.co/profile/rallyup), verified 5.0, PrettyDamnQuick, November 2026. Attribute to
"Haim Moskowitz, PrettyDamnQuick" (no job title: the case study says Head of Marketing, Clutch says Marketing Manager) and link the Clutch profile (an owner-approved exception
to rule 3: Haim is already named on the case study):
- Quote: "The audience got more senior."
- Reach among decision-makers up 50%; daily engagements doubled.
- Month one: 20,000+ impressions, about 2x reach per post (case-study figure) vs the previous baseline, 70+ new followers.
- Monthly lists of ICP-fit engagers that the sales team followed up on.

Client review on Clutch, verified 5.0, LetsGo, November 2026. Attribute to "CEO, LetsGo" (no name):
- "Significantly increased reach and brand recognition on LinkedIn."; "Hustle and passion for client's success!"
- Case-study numbers (Jul 7 - Sep 14, 2026, vs the 180 days before, n=10 posts): 2.4x impressions per post
  (5,112 to 12,493), 162,403 impressions, +378 followers, 849 engagements on the launch post. Hundreds of waitlist sign-ups at launch (first 100 spots
  in under 24 hours). After a B2C-to-B2B pivot, first enterprise customers (per Francisco, 2026-11-15).

Other approved client facts (owner-approved 2026-11-18):
- Anchor Browser (CEO): $550k in inbound pipeline generated from LinkedIn (a closed deal is NOT confirmed: never write "deal landed" or "won", decided 2026-11-23); 100 connection requests off one post.
- Andel (founder & CEO): 422k impressions in the first 2 months.
- First drafts land within 48 hours of onboarding.
- Cadence: the standard is 3 posts a week. Never quote the old 2.1 median as our cadence.
- Engagement (replying to comments, handling DMs) is NOT in the base plan; it is an add-on (decided
  2026-11-23). Never say engagement is included.
- A monthly list of ICP-fit people who engaged with the executive's posts, for the client's sales team to follow up, IS in the base plan (decided 2026-11-26). Say it plainly; it is separate from the comment/DM engagement add-on.
- rallyup works on LinkedIn and X. The guarantee and the benchmarks are LinkedIn-only.

## The monthly procedure

The method (adopted 2026-11-24, from Granola's AEO playbook): start from buyer decisions, not
keywords; diagnose every missed recommendation before writing anything; fix existing pages before
creating new ones; tie technical work to buying questions; study the sources AI already trusts;
show up where buyers already talk; measure Google and AI separately; retest and close the gaps.
Every action fits one of four jobs: **OWN** (our pages say clearly what rallyup does and who it
serves), **CLAIM** (specific, supportable advantages), **EARN** (independent coverage: reviews,
lists, mentions) and **CONTEST** (the alternatives buyers weigh, and the trade-offs).

The buyer decisions live in `aeo/decisions.json`: one entry per decision, with its stage, a
Google keyword, the AI prompts and the page that should win it. It is the only prompt list; edit
it there. Branded decisions (`"branded": true`) are reported separately and never count toward
the scorecard.

Work on a branch `aeo/YYYY-MM`. Keep notes as you go; they become the PR description and
`aeo/log/YYYY-MM.md`.

### 1. Measure Google and AI separately (about 30 minutes)

**AI answers.** For the first prompt of every decision, run a web search (mode standard, in
parallel batches) and save every result as aeo-outreach citation rows
(`engine: "claude"`, `prompt`, `url`, `domain`, `date`, `answer_mentions_us`, `competitors`) to
`rallyupcontext/data/aeo-outreach/citations/claude-YYYY-MM-DD.json`. Set `answer_mentions_us` true
only if the search's answer text names rallyup. Add the latest Otterly export if there is one
(six engines; better than our single-engine sweep).

**Google.** If Search Console access works, record clicks, impressions and average position for
each decision's `keyword` over the last 28 days. If it doesn't, say so in the PR; never fill the
column from the web search above (ranking on Google is not the same as being named by AI).

**Google's own AI count.** Search Console has a Generative AI performance report (Performance →
Generative AI; all sites since 2026-08-31). It counts how often rallyup.team URLs appeared in AI
Overviews and AI Mode: impressions only, no clicks, and AI Mode clicks stay inside the normal Web
totals. Record the 28-day total and the top 10 pages by AI impressions in the log, and compare each
decision's page with its bucket from step 2: a page Google shows in AI answers but our sweep marks
NOT-RETRIEVED is a sampling gap, not a page problem. If the report or its export isn't reachable,
say so in the PR; don't estimate it. Also confirm Settings → Search generative AI still reads
"Current control: Include" (checked 2026-11-26, inherited from the rallyup.team domain property);
if it ever reads Exclude, stop and tell Francisco before anything else.

**The five numbers**, each in the log with its source, every month:
1. Monthly new users from AI search (GA4 property 534101849: sessions whose source is chatgpt.com,
   perplexity.ai, claude.ai, gemini.google.com or copilot.microsoft.com).
2. Non-branded AI citations: citation share from step 2 (decision x engine answers citing a
   rallyup.team page).
3. Non-branded AI mentions: mention share from step 2 (answers that name rallyup).
4. Organic Google sessions (GA4, organic search).
5. Google AI impressions: the Generative AI report's 28-day total (above).
Plus bookings: the `website_ai` count (**tracked**) and tracked x 3 (**estimated**, an unverified
rule of thumb from the AEO expert call of 2026-11-18 that about 70% of AI-influenced buyers Google
the brand instead of clicking). Track total inbound bookings against the November 2026 baseline,
so growth isn't credited to AEO alone.

### 1b. Mine buyer questions and objections from sales calls

Sales call transcripts live in the private `rallyupcontext` repo, checked out alongside this one
(look for a sibling folder named `rallyupcontext`). Read the files in
`rallyupcontext/transcripts/sales/` whose `created:` date is in the last 30 days. Pull out:
- the questions prospects asked about LinkedIn ghostwriting (price, results, time commitment,
  voice, ghostwriter vs agency, what month one looks like, and so on);
- the objections they raised, and what they said they liked.

Use them to pick new pages, sharpen short answers and FAQs, and add `.limits` lines where an
objection shows a real fit question.

- Record **only the question, rewritten in generic words**, under "Page ideas" in
  `aeo/backlog.md`, tagged `(from calls)`. Note in the log how many calls asked something similar.
- **Never** write down a name, company, deal detail, number or quote from a call, in any file,
  the PR or Slack. Call content is private; the repo and the PR are public.
- If the `rallyupcontext` checkout is missing, skip this step and say so in the PR and the Slack DM.

### 2. Diagnose every miss

```
python3 aeo/diagnose.py <rallyupcontext>/data/aeo-outreach/citations/<this month's files> \
  --out aeo/log/YYYY-MM-diagnosis.md
```

This repo is public: never pass `--tracker` when writing to `aeo/log/`. Outreach status (who we
pitched) stays in rallyupcontext; run with `--tracker` to a scratch file when you need it.

It puts every decision in one bucket (WINNING, CITED-NOT-NAMED, NOT-RETRIEVED, NO-PAGE, TOO-NEW,
NOT-MEASURED) and lists, per decision, who was named instead, the sources engines used, the
third-party pages to EARN a place on, and the community threads where buyers talk.

Then, for every decision that isn't WINNING, open the top two sources the engines used and write
one line in the log: what they answer that our page doesn't. That line decides the fix; a bucket
alone doesn't.

**Retest.** Open last month's `aeo/log/*-diagnosis.md` and its "Actions taken" list. For each
action, say whether that decision's bucket moved. Keep what worked; rethink what didn't after two
months without movement.

### 3. Act by bucket, existing pages first

| Bucket | Job | What to do |
|---|---|---|
| CITED-NOT-NAMED | CLAIM | Engines read our page and still named others. Make the short answer state *why* rallyup fits, with approved facts (price, guarantee, benchmark with its sample size, a matching case study), and link the outside proof (Clutch, case study). |
| NOT-RETRIEVED | OWN + technical | Match the title, H1 and short answer to the buyer's phrasing. Add 2+ internal links from the decision pages before and after it in the buyer journey. Confirm it returns 200 to GPTBot, ClaudeBot and PerplexityBot and is in `sitemap.xml`. |
| NO-PAGE | OWN | Add a section or an FAQ (visible and JSON-LD) to the closest existing page, then set that page in `decisions.json`. A new page only if no existing page can carry the answer; say why in the PR. |
| TOO-NEW | none | Leave it. Retest next month. |
| WINNING | defend | Keep its facts current. No date bump without a real change. |
| EARN list | EARN | Don't pitch from this run. List the domains in the PR; the `aeo-outreach` skill in rallyupcontext handles pitching, with Francisco sending. |
| where buyers talk | EARN | Draft (never post) up to 3 replies a month to the Reddit threads or LinkedIn posts the engines cite, for Francisco or Alec to post under their own name, saying they run rallyup. Each reply must answer the thread's question usefully on its own; no links unless the thread asks for one. |
| named instead, 3+ engines | CONTEST | If a competitor is named instead of us in 3+ engines and we have no alternatives page for it, propose one in the PR. |

Write **at most 2 new pages a month**, and only for NO-PAGE decisions no existing page can carry,
or a CONTEST proposal Francisco approved. More pages is not the goal; closing gaps is.

Record every change in the log under **"Actions taken (retest next month)"**: decision id, bucket,
what changed, on which page. Next month's step 2 reads that list.

### 4. Refresh comparison pages and stale pages

Run `python3 aeo/check.py`. Then:

1. **Comparison pages** (`best-*`, `*-alternatives`, `linkedin-ghostwriting-cost-2026`,
   `linkedin-post-writing-cost-per-post`): these promise a monthly price check. For every
   competitor named, fetch their own pricing and services page and fix anything that changed.
   If WebFetch can't reach a site, fetch it with Bash instead
   (`curl -sL -m 20 -A "Mozilla/5.0" <url>`) and read the text out of the HTML. Only list a
   competitor under "Couldn't verify" if both fail.
   If a competitor closed or no longer offers the service, remove it and log the removal.
2. **Pages flagged STALE** by `check.py` (dateModified over 90 days): re-read, update any fact
   that has aged, tighten the short answer.

For every page you change, and only those:
- add a dated line to its `.changelog` saying what changed in plain words;
- set `dateModified` in the JSON-LD and the "last updated" line to this month;
- set its `<lastmod>` in `sitemap.xml` to today.

Do not bump dates on pages you didn't materially change. Fake freshness is easy to detect and
costs trust, and Google tells site owners not to change a page's date unless its content
substantially changed. **What moves the date:** a new or rewritten section, a new or changed fact
(price, offer, guarantee, a competitor's price or service, a number), a competitor added or
removed, or a new FAQ answer. **What doesn't:** wording or typo fixes, links, styling, an author box,
schema-only edits. Those still get a changelog line if a reader would notice, but that line starts
with "Minor:" and the date stays where it was. Batch small edits into the monthly run instead of
bumping a page several days in a row.

`check.py` enforces the mechanics: `dateModified` must equal the newest dated changelog line, and
the visible "updated" date and the sitemap `<lastmod>` must match it. Never change an old changelog
date to get past the check.

New pages (step 3 cap applies). For each page:
1. Write `aeo/specs/<slug>.json` (format: `aeo/specs/example-linkedin-ghostwriter-vs-agency.json`,
   plus `card_tag`, `card_blurb` and `llms_line`). The changelog line is "first published <date>".
2. `python3 aeo/build_page.py aeo/specs/<slug>.json` builds `blog/<slug>.html` and adds it to
   `sitemap.xml`, `llms.txt` and the blog index.
3. Link to it from 1 or 2 related existing pages.
4. Move the idea from "Page ideas" to "Published" in `aeo/backlog.md`, and set the page on its
   decision in `aeo/decisions.json`.

### 4b. Weak or outdated pages: consolidate, don't delete

If two pages answer the same question, or a page's decision has sat in NOT-RETRIEVED for 2+ months
and the page has nothing unique, do not delete it. Instead, propose in the PR (don't do it
yourself): merge its best content into the stronger page and turn the weaker one into a short
pointer with `<link rel="canonical">` to the stronger URL. Francisco decides.

Year-stamped pages ("... 2026"): in December, propose the January refresh. Keep the URL, update
the title, headline and content to the new year, and log it in the changelog.

### 5. Validate

`python3 aeo/check.py` must exit 0. Fix every ERROR. Then serve the site locally
(`python3 -m http.server 8791`) and open each new or changed page to confirm it renders.

### 6. Open the PR

Commit to `aeo/YYYY-MM`, push, and open a PR to `main` titled `AEO YYYY-MM`. The description:

- **Scorecard**: non-branded mention share and citation share (step 2), this month vs last; the
  five numbers from step 1; branded reported on its own line.
- **Bucket moves**: decisions that changed bucket, and the action that preceded each.
- **New pages**: URL, author, the question it answers.
- **Refreshed pages**: what changed on each, with the source URL for every competitor fact.
- **Couldn't verify**: anything you left out and why.
- **Proposals**: consolidations or bigger changes for Francisco to decide.
- **LinkedIn drafts**: one short post per new page for Francisco or Alec to adapt, linking the
  page. Plain, first person, no hashtags, no em dashes.

### 7. Tell Francisco

Send a Slack DM to Francisco (user ID `U0A0TKY82D8`): the PR link, the scorecard line, the number
of new and refreshed pages, and anything that needs his decision. Keep it under 8 lines.

### Quarterly (February, May, August, November)

Add one line to the Slack DM: "Benchmark report refresh is due." Don't recompute the benchmark
yourself; it needs Ordinal data and a human check before anything is published.
