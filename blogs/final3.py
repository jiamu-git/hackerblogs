import csv, json, sys, math, collections
import duckdb
sys.path.insert(0, 'blogs')
from classify import DROP, TEAM_EXTRA

BIG = set("""amazon.com google.com microsoft.com apple.com facebook.com twitter.com
wikipedia.org youtube.com github.com gitlab.com linkedin.com reddit.com
cloudflare.com mozilla.org adobe.com oracle.com ibm.com intel.com nvidia.com
samsung.com sony.com netflix.com paypal.com ebay.com yahoo.com bing.com
medium.com quora.com stackoverflow.com blogspot.com wordpress.com tumblr.com
nytimes.com bloomberg.com reuters.com wsj.com forbes.com businessinsider.com
""".split())

def is_big(d):
    return any(d == b or d.endswith('.' + b) for b in BIG)

live = {x['domain']: x for x in json.load(open('blogs/liveness.json'))}
cand = {r['domain']: r for r in csv.DictReader(open('blogs/candidates.csv'))}
con = duckdb.connect()
med = {d: (m, p, n) for d, m, p, n in con.execute(
    "SELECT d, med, p90, n FROM 'blogs/domain_medians.parquet'").fetchall()}

rows = []
for d, L in live.items():
    if not L.get('ok') or d in DROP or is_big(d): continue
    r = cand[d]
    m, p90, n = med.get(d, (0, 0, 0))
    quality = min(p90 or 0, 600)
    if quality < 40: continue                    # nothing ever scored well
    hi = int(r['hi']) if 'hi' in r else 0
    yrs = int(r['yrs']); mentions = int(r['cmt'])
    persistence = 0.4 + min(yrs, 12) / 12
    popularity = 1 + min(math.log10(1 + mentions), 3) / 4
    volume = 1 + min(int(r['sub_n']), 40) / 40 * 0.3
    score = quality * persistence * popularity * volume
    rows.append({'domain': d, 'feed': L.get('feed'), 'category':
                 '团队/工程博客' if d in TEAM_EXTRA else '个人博客',
                 'posts': int(r['sub_n']), 'avg': float(r['avg']), 'p90': round(p90 or 0, 1),
                 'years': yrs, 'first': r['first'], 'last': r['last'],
                 'mentions': mentions, 'score': round(score, 1),
                 'title': (L.get('title') or '')[:80]})
rows.sort(key=lambda r: -r['score'])
with open('blogs/final.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
feed_rows = [r for r in rows if r['feed']]
print(f"reachable blogs: {len(rows)}, with feed: {len(feed_rows)}")

def esc(s): return (s or '').replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')
with open('blogs/no-feed.csv','w',newline='') as fh:
    rest=[r for r in rows if not r['feed']]
    w=csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rest)

out = ['<?xml version="1.0" encoding="UTF-8"?>', '<opml version="2.0">', '  <head>',
       '    <title>HN Independent Blog Index</title>', '  </head>', '  <body>']
groups = [('精选 Top 300', feed_rows[:300]), ('完整 · 全部有 feed', feed_rows)]
for gname, glist in groups:
    out.append(f'    <outline text="{gname}" title="{gname}">')
    for r in glist:
        t = f"{r['domain']} · {r['posts']} posts · p90 {r['p90']} · {r['first']}-{r['last']}"
        out.append(f'      <outline type="rss" text="{esc(t)}" title="{esc(r["domain"])}" '
                   f'xmlUrl="{esc(r["feed"])}" htmlUrl="https://{esc(r["domain"])}"/>')
    out.append('    </outline>')
out += ['  </body>', '</opml>']
open('blogs/hn-blogs.opml','w').write("\n".join(out))
print(collections.Counter(r['category'] for r in feed_rows))
print("no-feed listed:", len(rest))
