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
- Anchor Browser (CEO): $550k in inbound pipeline opened from LinkedIn (a closed deal is NOT confirmed: never write "deal landed" or "won", decided 2026-11-23); 100 connection requests off one post.
- Andel (founder & CEO): 422k impressions in the first 2 months.
- First drafts land within 48 hours of onboarding.
- Cadence: the standard is 3 posts a week. Never quote the old 2.1 median as our cadence.
- Engagement (replying to comments, handling DMs) is NOT in the base plan; it is an add-on (decided
  2026-11-23). Never say engagement is included.
- rallyup works on LinkedIn and X. The guarantee and the benchmarks are LinkedIn-only.

## The monthly procedure

Work on a branch `aeo/YYYY-MM`. Keep notes as you go; they become the PR description and
`aeo/log/YYYY-MM.md`.

### 1. Measure (about 20 minutes)

For each prompt under "Tracking prompts" in `aeo/backlog.md`, run a web search and record:
- whether any rallyup.team page appears in the results, and which;
- the 3 to 5 domains that appear most (these are what AI engines cite).

Write a table to `aeo/log/YYYY-MM.md`: prompt, rallyup page found (or none), top cited domains.
Compare with last month's log if one exists and note what moved.

Also record, from the bookings dashboard, the month's bookings tagged `website_ai` (visitors who
arrived from ChatGPT, Perplexity, Claude, Gemini or Copilot) and total inbound bookings. Report AI's
influence two ways, and label them:
- **tracked:** the `website_ai` count, which is verified.
- **estimated:** tracked × 3, which is an assumption. It rests on the AEO expert's rule of thumb
  (2026-11-18) that about 30% of people click the link in an AI answer and about 70% Google the
  brand instead, and we haven't verified it. Always print the word "estimated" next to it.
Track total inbound bookings against the November 2026 baseline, so growth isn't credited to AEO
alone.

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

### 2. Refresh what exists

Run `python3 aeo/check.py`. Then refresh, in this order:

1. **Comparison pages** (`best-*`, `*-alternatives`, `linkedin-ghostwriting-cost-2026`,
   `linkedin-post-writing-cost-per-post`): these promise a monthly price check. For every
   competitor named, fetch their own pricing and services page and fix anything that changed.
   If WebFetch can't reach a site, fetch it with Bash instead
   (`curl -sL -m 20 -A "Mozilla/5.0" <url>`) and read the text out of the HTML. Only list a
   competitor under "Couldn't verify" if both fail.
   If a competitor closed or no longer offers the service, remove it and log the removal.
2. **Pages flagged STALE** by `check.py` (dateModified over 90 days): re-read, update any fact
   that has aged, tighten the short answer.
3. **Pages for prompts where rallyup was not found** in step 1: improve the short answer so it
   matches how the prompt is phrased, and add the missing question to the FAQ.

For every page you change, and only those:
- add a dated line to its `.changelog` saying what changed in plain words;
- set `dateModified` in the JSON-LD and the "last updated" line to this month;
- set its `<lastmod>` in `sitemap.xml` to today.

Do not bump dates on pages you didn't materially change. Fake freshness is easy to detect and
costs trust.

### 3. Add new pages (4 to 6)

Pick from `aeo/backlog.md` "Page ideas", plus any gaps step 1 surfaced: a tracking prompt where
rallyup is absent and no existing page answers it, or a question competitors' pages answer that
ours don't. Prefer specific buyer questions ("how much does a CEO ghostwriter cost in the UK")
over broad ones. Skip a topic if you can't support the page with approved facts and verified
sources; say so in the PR rather than writing a thin page.

For each page:
1. Write `aeo/specs/<slug>.json` (format: `aeo/specs/example-linkedin-ghostwriter-vs-agency.json`,
   plus `card_tag`, `card_blurb` and `llms_line`). The changelog line is "first published <date>".
2. `python3 aeo/build_page.py aeo/specs/<slug>.json` builds `blog/<slug>.html` and adds it to
   `sitemap.xml`, `llms.txt` and the blog index.
3. Link to it from 1 or 2 related existing pages.
4. Move the idea from "Page ideas" to "Published" in `aeo/backlog.md`.

### 4. Weak or outdated pages: consolidate, don't delete

If two pages answer the same question, or a page has gone 2+ months without appearing in any
tracking search and has nothing unique, do not delete it. Instead, propose in the PR (don't do it
yourself): merge its best content into the stronger page and turn the weaker one into a short
pointer with `<link rel="canonical">` to the stronger URL. Francisco decides.

Year-stamped pages ("... 2026"): in December, propose the January refresh. Keep the URL, update
the title, headline and content to the new year, and log it in the changelog.

### 5. Validate

`python3 aeo/check.py` must exit 0. Fix every ERROR. Then serve the site locally
(`python3 -m http.server 8791`) and open each new or changed page to confirm it renders.

### 6. Open the PR

Commit to `aeo/YYYY-MM`, push, and open a PR to `main` titled `AEO YYYY-MM`. The description:

- **Scorecard**: tracking prompts where rallyup appears, this month vs last month.
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
