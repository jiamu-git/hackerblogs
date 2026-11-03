# Hacker Blogs

Twenty years of Hacker News taste, turned into something you can browse and subscribe to.

- **4,790** sites, mined from 6,236,741 submissions (**4,400** blogs, 390 company or org sites)
- **3,500** most-cited posts, filtered from 13,589,826 URL mentions across 43,051,020 comments
- **2,241** feeds you can subscribe to today

The layout follows [Hacker Books](https://news.ycombinator.com/) (card wall plus faceted sidebar).
The visual language is a different thing: a **library card catalog printed on warm paper**.
Static, zero build, drops straight onto GitHub Pages.

## Curation

A raw HN domain ranking is full of product pages, language homepages and corporate blogs.
Three passes keep the catalog honest:

| Pass | Rule | Result |
|---|---|---|
| Structural | 30% or more of a domain's submissions land on its root path, or 25% on download, changelog, pricing or release paths | 526 dropped |
| Content | every site sampled: feed items when a feed exists, otherwise its 12 highest-scoring HN submission titles plus the homepage title and description | 306 products dropped, 390 company tagged |
| Hand review | product, project, language, mail-archive and media domains read one by one from the top of the ranking | 288 corrections |

A site is only called a **blog** when there is positive evidence: a feed of at least three posts
with under 30% release notes and a median title length of three words or more, or explicit blog
wording on the page. Anything without evidence leaves the main list instead of being assumed
personal. That default was the bug in the first version: 4,996 sites were labelled personal when
only 600 had ever been looked at. A 20-site sample showed roughly 45% of them were wrong.

Homepage markers were tried first and rejected: JavaScript-rendered product pages show no CTAs in
the HTML, and `kalzumeus.com` looks exactly like a product page on those signals.

### Measured accuracy

| Slice | Correct | Method |
|---|---|---|
| Top 150 by score | about 97% | hand-checked |
| Random sample of 25 from the rest | about 80% | hand-checked |

The error that survives is the hardest one: a company engineering blog reads exactly like a
personal blog. `nvidia.github.io` and `shopify.github.io` pass every content test. Telling them
apart needs knowledge of who publishes the site, not a better regex.

## Landing page

The most-cited post list is the home view. The blog catalog sits behind **All blogs**, and
**Subscribable** narrows it to sites with a feed. There is no separate daily shelf any more;
the catalogue is reached in one click instead of competing with it for the first screen.

## OPML

Two flat files, no nested groups, so importing one never creates duplicates:

| File | Feeds | Use |
|---|---|---|
| `hn-blogs.opml` | 2,241 | the whole catalogue |
| `hn-blogs-top300.opml` | 300 | a smaller starting set |

Both are linked from the sidebar under **Subscribe by RSS**, stacked so the label fits on one line.
On mobile they collapse into a two-button row under the nav. The top bar carries only the
language switch.

Entries are deduplicated by feed URL, so two domains pointing at the same feed appear once.

## Post list

3,500 posts, paginated at 100 per page (35 pages), with a global rank number that continues
across pages (page two starts at 101).

Filters: **topic** (derived from the post title, falling back to the domain's subject) and
**year span**. Both recalculate the page count and reset to page one. First, Previous, Next and
Last are keyboard reachable; the outer two are hidden below 640px.

## Descriptions

Every site has a one-line intro shown in its detail panel. 741 come from the site itself (its meta
description) or from a hand-written line for the top 60, the rest are generated from data:
`17 posts on Hacker News between 2020 and 2023, mostly science and ideas.`

## Design direction

- **The card is data, not decoration.** Every card shows 21 bars, one per year from 2006 to 2026.
  A filled bar means the site was submitted that year; an empty one leaves a tick on the baseline.
  The wall becomes a scannable map of when things were alive.
- **Colour is classification, not randomness.** Eleven subjects own eleven inks (OKLCH).
  The sidebar dot, the card band and the drawer mark share the exact same value.
- **No shadows, only hairlines.** Cards separate by a 1px rule and a paper tint.
  The only shadow belongs to the drawer that slides in from the right.
- **One accent, used sparingly.** Stamp red marks years and `No feed`. It never fills a surface.

## Language

The UI ships **English by default** and switches to Chinese from the `EN / 中文` control in the top bar.

- Choice persists in `localStorage` under `hb-lang`
- `<html lang>`, `<title>` and the meta description update with the switch
- All copy lives in `I18N` in [`assets/app.js`](assets/app.js); subject names in `SUBJECT_LABELS` and `SUBJECT_SHORT`
- Numbers and dates follow the locale (`en-US` / `zh-CN`)

To add a third language: add a key to `I18N`, `SUBJECT_LABELS`, `SUBJECT_SHORT`, then add a button
to the `.lang` group in `index.html`.

## Local preview

```bash
cd site
python3 -m http.server 8791
# open http://127.0.0.1:8791/
```

No build step, no npm, no framework. Edit HTML/CSS/JS and refresh.

## Layout

```
site/
├── index.html          single page shell, all copy carries data-i18n keys
├── assets/
│   ├── style.css       tokens, card catalog, drawer
│   └── app.js          i18n, render, filter, search, drawer (vanilla, no deps)
├── data/
│   ├── blogs.json      4,790 sites (2.1 MB)
│   ├── posts.json      3,500 posts (547 KB)
│   ├── hn-blogs.opml          2,241 feeds, flat, no duplicates
│   └── hn-blogs-top300.opml   300 feeds, the highest scoring
├── build_data.py       regenerate data/ from blogs/*.csv and parquet
└── .nojekyll           skip Jekyll processing
```

## Deploy to GitHub Pages

**Option A: Actions (already configured)**

1. Push to `main`
2. Repo Settings → Pages → Source: **GitHub Actions**
3. Once the workflow finishes, the site is at `https://<user>.github.io/<repo>/`

Every later change under `site/**` redeploys automatically.

**Option B: no Actions**

Settings → Pages → Source: `Deploy from a branch`, branch `main`, folder **`/docs`**.
That means renaming `site/` to `docs/`.
Do not pick `/root`: it would publish the whole repository, mining data included.

## Where the data comes from

The full pipeline lives in `blogs/`. Its CSV and parquet outputs feed this site.

| Signal | Source | Volume |
|---|---|---|
| Submission | the `url` field of every story, grouped by domain | 5,268,724 |
| Discussion | URLs extracted from comment text, HTML entities decoded | 13,589,826 |
| Liveness | one homepage fetch per domain, feed read from `<link rel=alternate>` | 23,312 domains |

**Ranking:**

```
score = min(p90, 600) × (0.4 + min(years,12)/12) × (1 + min(log10(1+mentions),3)/4) × (1 + min(posts,40)/40×0.3)
```

`p90` is the 90th percentile of scores across a domain's submitted pages, which resists one-hit outliers.
The post list ranks on **distinct years cited** instead: fifteen years of repeats is what makes a classic.

## Refreshing the data

```bash
python3 site/build_data.py     # rebuild JSON from blogs/
```

For the whole pipeline (download the dataset, rescan, re-probe), see
`blogs/pass_a.py`, `blogs/pass_b.py` and `blogs/liveness.py`.

The dataset is [open-index/hacker-news](https://huggingface.co/datasets/open-index/hacker-news),
ODC-BY, updated every five minutes.

## Known gaps

- **Reachable is not alive.** A dead blog still returns 200 on its homepage.
- **Subject tags are keyword-derived, not hand-labelled**, so a few are wrong.
- **Comment coverage is link-only** (5.16M of 43.05M comments contain a URL); plain-text recommendations are missed.
- A handful of product pages and project sites are still mixed into the list.
