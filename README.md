# Hacker Blogs

A catalogue of independent blogs and the posts Hacker News keeps citing, mined from the
complete HN archive: 6,236,741 submissions and 43,051,020 comments.

**4,790 sites** (4,398 blogs, 392 company or org blogs) and **3,500 most-cited posts**.

Live: https://jiamu-git.github.io/hackerblogs/

## What is in here

```
site/                 the static site, no build step
  index.html
  assets/             style.css, app.js
  data/               blogs.json, posts.json, two OPML files
  build_data.py       regenerates data/ from blogs/
  README.md           design notes, deploy notes, known gaps
blogs/                the mining pipeline and its outputs
  *.py                scan, classify, curate, report
  final.csv           the curated catalogue
  verdicts.py         hand-reviewed product / company decisions
.github/workflows/    GitHub Pages deploy
```

## The pipeline

| Step | Script | What it does |
|---|---|---|
| 1 | `blogs/pass_a.py` | per-domain submission counts, scores, active years |
| 2 | `blogs/pass_b.py` | URLs mentioned inside comments, per domain and year |
| 3 | `blogs/liveness.py` | one homepage fetch per domain: reachable, plus feed discovery |
| 4 | `blogs/final3.py` | joins the signals into a ranked catalogue |
| 5 | `blogs/curate.py` | drops product pages by URL shape, tags orgs |
| 6 | `blogs/classify_sites.py` | content classification from feed items and HN titles |
| 7 | `blogs/apply_kinds.py` | applies the verdicts, emits OPML |
| 8 | `site/build_data.py` | emits the JSON the site loads |

## Deploying

Push to `main`. The workflow in `.github/workflows/pages.yml` publishes `site/` to GitHub Pages,
enabling Pages on the first run.

Locally: `cd site && python3 -m http.server 8791`.

## Data

Source: [open-index/hacker-news](https://huggingface.co/datasets/open-index/hacker-news), ODC-BY.
The catalogue is a derived work; the underlying posts and comments belong to their authors.

## Known gaps

- Roughly 80% of the catalogue is correctly classified; company engineering blogs that read like
  personal blogs are the hardest case. See `site/README.md` for the measured numbers.
- Comment coverage is link-only: 5.16M of 43M comments contain a URL.
- No liveness signal for sites without a feed.
