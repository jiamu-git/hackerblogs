import json, csv, sys, math
import duckdb
sys.path.insert(0, 'blogs')
from classify import is_blog, ORG_BLOGS

dom = json.load(open('blogs/domains.json'))
con = duckdb.connect(); con.execute("SET threads=4")
cmt = {}
for h, n, yrs, urls in con.execute("""
    SELECT lower(host) h, sum(n), count(DISTINCT yr), count(DISTINCT url)
    FROM 'blogs/comment_links.parquet' GROUP BY 1
""").fetchall():
    h = h[4:] if h.startswith('www.') else h
    c = cmt.setdefault(h, [0, 0, 0])
    c[0] += n; c[1] = max(c[1], yrs); c[2] += urls

rows = []
for d, s in dom.items():
    if not is_blog(d)[0]: continue
    c = cmt.get(d, [0, 0, 0])
    sustained = s['n'] >= 6 and s['nyears'] >= 3
    discussed = c[0] >= 100 and c[1] >= 3 and s['n'] >= 3
    if not (sustained or discussed): continue
    q = min(s['avg'], 400)
    p = min(s['nyears'], 12)
    score = q * (0.4 + p / 12) * (1 + min(math.log10(1 + c[0]), 3) / 4)
    rows.append({'domain': d, 'score': round(score, 1), 'sub_n': s['n'], 'sub_avg': s['avg'],
                 'sub_max': s['max'], 'sub_hi': s['hi'], 'sub_years': s['nyears'],
                 'first': s['first'], 'last': s['last'], 'recent': s['recent'],
                 'cmt_n': c[0], 'cmt_years': c[1], 'cmt_urls': c[2], 'org': d in ORG_BLOGS})
rows.sort(key=lambda r: -r['score'])
with open('blogs/ranked.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print("kept:", len(rows))
for r in rows[:120]:
    flag = "ORG" if r['org'] else "   "
    print(f"{r['score']:6.0f} {r['domain']:30s} {flag} n={r['sub_n']:4d} avg={r['sub_avg']:4.0f} "
          f"yrs={r['sub_years']:2d} cmt={r['cmt_n']:5d} [{r['first']}-{r['last']}]")
