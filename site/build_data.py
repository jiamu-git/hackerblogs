"""Build the static site's data files from the mined CSV/parquet outputs."""
import csv, json, math, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'blogs'))
from intros import INTROS
import duckdb

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, 'blogs')
OUT = os.path.join(ROOT, 'site', 'data')

blogs = list(csv.DictReader(open(os.path.join(B, 'final.csv'))))
domains = {b['domain'] for b in blogs}

con = duckdb.connect(); con.execute("SET threads=4")
rows = con.execute("""
  SELECT host, url, title, years, sub_n, best_score, cmt_n
  FROM 'blogs/post_canon.parquet'
  WHERE url IS NOT NULL AND title IS NOT NULL AND length(title) > 8
""").fetchall()

def norm(h):
    h = (h or '').lower()
    return h[4:] if h.startswith('www.') else h

posts = []
for host, url, title, years, sn, bs, cn in rows:
    h = norm(host)
    if h not in domains: continue
    if years < 2 or (bs or 0) < 20: continue
    path = url.split('/', 3)[3] if url.count('/') >= 3 else ''
    if len(path) < 3: continue
    posts.append({'d': h, 'u': url, 't': title.strip(), 'y': int(years),
                  's': int(bs or 0), 'm': int(cn or 0),
                  'sc': int(years * 3 + min(math.log10(1 + (cn or 0)), 3) * 4 + min((bs or 0) / 150, 3))})
posts.sort(key=lambda p: -p['sc'])
# cap per domain, keep top 3500
cap, seen, kept = 4, {}, []
for p in posts:
    if seen.get(p['d'], 0) >= cap: continue
    seen[p['d']] = seen.get(p['d'], 0) + 1
    kept.append(p)
    if len(kept) >= 3500: break

TOPICS = [
 ('安全与隐私', 'security hack exploit vulnerability cve malware reverse cracking cipher privacy surveillance'),
 ('系统与内核', 'kernel linux unix os filesystem file system memory allocator cpu scheduler driver emulator virtual machine qemu'),
 ('语言与编译器', 'compiler parser type system lisp haskell rust golang javascript interpreter language design programming language'),
 ('Web 与前端', 'css html browser javascript react frontend web http dom svg canvas'),
 ('数据与 AI', 'machine learning ml ai llm neural dataset database sql postgres storage query model training gpt transformer'),
 ('数学', 'math proof theorem algebra geometry number prime calculus statistics probability'),
 ('硬件与底层', 'hardware chip fpga electronics circuit retro computing z80 6502 microcontroller arduino raspberry pi cpu design'),
 ('设计', 'design ux typography interface usability interaction visual'),
 ('职业与创业', 'career salary hiring job interview startup founder business product management'),
 ('科学与思想', 'physics biology space astronomy neuroscience science philosophy economics history'),
]
def topics_for(texts):
    scores = {}
    for name, kw in TOPICS:
        kws = kw.split()
        n = sum(1 for t in texts for k in kws if k in t.lower())
        if n: scores[name] = n
    return sorted(scores, key=lambda k: -scores[k])[:2] or ['其他']

# all story titles per domain (top 25 by score) for topic inference
title_rows = con.execute("""
  WITH t AS (
    SELECT lower(regexp_replace(host,'^www\\.','')) AS d, title, score
    FROM 'blogs/story_urls.parquet' WHERE title IS NOT NULL AND length(title) > 6
  ), r AS (
    SELECT d, title, row_number() OVER (PARTITION BY d ORDER BY score DESC) rn FROM t
  )
  SELECT d, title FROM r WHERE rn <= 25
""").fetchall()
titles_by_domain = {}
for d, t in title_rows:
    if d in domains:
        titles_by_domain.setdefault(d, []).append(t)

by_domain = {}
for p in kept:
    by_domain.setdefault(p['d'], []).append(p)

for b in blogs:
    b['posts'] = int(b['posts']); b['p90'] = round(float(b['p90']), 1)
    b['years'] = int(b['years']); b['first'] = int(b['first']); b['last'] = int(b['last'])
    b['mentions'] = int(b['mentions']); b['score'] = round(float(b['score']), 1)
    b['has_feed'] = bool(b['feed'])
    ps = by_domain.get(b['domain'], [])
    texts = ([b['title'] or ''] + titles_by_domain.get(b['domain'], []) + [p['t'] for p in ps])[:40]
    b['topics'] = topics_for(texts)
    b['kind'] = b.get('kind') or 'blog'
    desc = INTROS.get(b['domain']) or (b.get('desc') or '').strip()
    if desc:
        b['intro'] = desc
    else:
        EN = {'系统与内核': 'systems and kernels', '数据与 AI': 'data and AI',
              '语言与编译器': 'languages and compilers', '硬件与底层': 'hardware',
              'Web 与前端': 'the web', '安全与隐私': 'security and privacy',
              '职业与创业': 'careers and startups', '设计': 'design',
              '科学与思想': 'science and ideas', '数学': 'math'}
        top = b['topics'][0] if b['topics'] else ''
        b['intro'] = (f"{b['posts']} posts on Hacker News between {b['first']} and {b['last']}"
                      + (f", mostly {EN[top]}" if top in EN else '') + '.')
    b.pop('desc', None)
    b['pcount'] = len(ps)

import shutil
shutil.copy(os.path.join(B, 'hn-blogs.opml'), os.path.join(OUT, 'hn-blogs.opml'))
# year-active bitmask (2006..2026) for the lifespan strip
_years = {}
try:
    _dom = json.load(open(os.path.join(B, 'domains.json')))
    for d, v in _dom.items():
        _bits = 0
        for y in v.get('years', []):
            if 2006 <= y <= 2026:
                _bits |= 1 << (y - 2006)
        _years[d] = _bits
except Exception as e:
    print('years unavailable:', e)

for b in blogs:
    b['ya'] = _years.get(b['domain'], 0)

json.dump(blogs, open(os.path.join(OUT, 'blogs.json'), 'w'), separators=(',', ':'))
# per-post topic: the post's own title first, the domain's subject as fallback
dom_topic = {b['domain']: (b['topics'][0] if b['topics'] else '其他') for b in blogs}
for p in kept:
    tp = topics_for([p['t']])
    p['tp'] = tp[0] if tp and tp[0] != '其他' else dom_topic.get(p['d'], '其他')
json.dump(kept, open(os.path.join(OUT, 'posts.json'), 'w'), separators=(',', ':'))
print(f"blogs={len(blogs)} posts={len(kept)} domains_with_posts={len(by_domain)}")
import collections
print(collections.Counter(t for b in blogs for t in b['topics']).most_common())
print("size:", os.path.getsize(os.path.join(OUT,'blogs.json'))//1024, "KB /",
      os.path.getsize(os.path.join(OUT,'posts.json'))//1024, "KB")
