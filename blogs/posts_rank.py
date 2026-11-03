import csv, math, sys, json
import duckdb
sys.path.insert(0,'blogs')
from classify import is_blog

final = {r['domain'] for r in csv.DictReader(open('blogs/final.csv'))}
con = duckdb.connect(); con.execute("SET threads=4")
rows = con.execute("""
SELECT url, host, title, sub_years, sub_n, best_score, cmt_n, cmt_years, years
FROM 'blogs/post_canon.parquet'
WHERE url IS NOT NULL
""").fetchall()

def norm(h):
    if not h: return ''
    h = h.lower()
    return h[4:] if h.startswith('www.') else h

blog_posts, other_posts = [], []
for url, host, title, sy, sn, bs, cn, cy, years in rows:
    h = norm(host)
    if not h: continue
    score = years * 3 + min(math.log10(1 + (cn or 0)), 3) * 4 + min((bs or 0) / 150, 3)
    rec = {'url': url, 'host': h, 'title': title, 'years': years, 'sub_n': sn,
           'cmt_n': cn or 0, 'best': bs or 0, 'score': round(score, 2)}
    if h in final:
        blog_posts.append(rec)
    elif is_blog(h)[0]:
        other_posts.append(rec)

blog_posts.sort(key=lambda r: -r['score'])
other_posts.sort(key=lambda r: -r['score'])
with open('blogs/posts_from_list.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(blog_posts[0].keys())); w.writeheader()
    w.writerows(blog_posts[:300])
with open('blogs/posts_global.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(other_posts[0].keys())); w.writeheader()
    w.writerows(other_posts[:300])

print("=== posts from the 120 blogs (top 25) ===")
for r in blog_posts[:25]:
    print(f"{int(r['years']):2d}y {int(r['cmt_n']):5d}m {int(r['best']):4d}p | {r['host']:28s} | {(r['title'] or r['url'])[:70]}")
print("\n=== top multi-year posts globally (top 25) ===")
for r in other_posts[:25]:
    print(f"{int(r["years"]):2d}y {int(r["cmt_n"]):5d}m {int(r["best"]):4d}p | {r['host']:28s} | {(r['title'] or r['url'])[:70]}")
