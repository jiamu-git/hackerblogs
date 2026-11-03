"""Merge submission stats + comment mentions, classify, rank."""
import json, csv, sys
import duckdb
sys.path.insert(0, 'blogs')
from classify import is_blog, ORG_BLOGS

dom = json.load(open('blogs/domains.json'))
con = duckdb.connect()
con.execute("SET threads=4")

cmt = {}
for host, n, yrs, urls in con.execute("""
    SELECT lower(host) AS h, sum(n) AS mentions,
           count(DISTINCT yr) AS cmt_years, count(DISTINCT url) AS urls
    FROM 'blogs/comment_links.parquet'
    GROUP BY 1
""").fetchall():
    h = h = host
    if h.startswith('www.'):
        h = h[4:]
    c = cmt.get(h)
    if c:
        c[0] += n; c[1] = max(c[1], yrs); c[2] += urls
    else:
        cmt[h] = [n, yrs, urls]

rows = []
for d, s in dom.items():
    keep, reason = is_blog(d)
    if not keep:
        continue
    c = cmt.get(d, [0, 0, 0])
    if s['n'] < 3 and c[0] < 15:
        continue
    if s['nyears'] < 2 and c[1] < 2:
        continue
    # persistence: distinct years seen in either channel
    span = max(1, s['last'] - s['first'] + 1)
    rows.append({
        'domain': d,
        'sub_n': s['n'],
        'sub_avg': s['avg'],
        'sub_max': s['max'],
        'sub_hi': s['hi'],
        'sub_years': s['nyears'],
        'first': s['first'],
        'last': s['last'],
        'recent': s['recent'],
        'cmt_n': c[0],
        'cmt_years': c[1],
        'cmt_urls': c[2],
        'org': d in ORG_BLOGS,
        'score': round(s['avg'] * (1 + s['nyears'] / 10) + min(c[0], 5000) / 50, 1),
    })

rows.sort(key=lambda r: -r['score'])
with open('blogs/ranked.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print("domains kept:", len(rows))
print("\nTOP 60 by hybrid score:")
for r in rows[:60]:
    print(f"  {r['score']:7.1f} | {r['domain']:34s} sub={r['sub_n']:4d} avg={r['sub_avg']:5.0f} "
          f"yrs={r['sub_years']:2d} cmt={r['cmt_n']:5d} [{r['first']}-{r['last']}]")
