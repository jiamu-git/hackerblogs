import json, csv, sys, collections
sys.path.insert(0, 'blogs')
from classify import DROP, TEAM_EXTRA

probe = {x['domain']: x.get('feed') for x in json.load(open('blogs/probe_result.json'))}
cand = {r['domain']: r for r in csv.DictReader(open('blogs/candidates.csv'))}
rows = []
for d, feed in probe.items():
    if not feed or d in DROP: continue
    r = cand[d]
    rows.append({'domain': d, 'feed': feed,
                 'category': '团队/工程博客' if d in TEAM_EXTRA else '个人博客',
                 'posts': int(r['sub_n']), 'avg_score': float(r['avg']),
                 'years': int(r['yrs']), 'first': r['first'], 'last': r['last'],
                 'mentions': int(r['cmt'])})
rows.sort(key=lambda r: -float(r['avg_score']) * (1 + r['years'] / 12) * (1 + min(r['mentions'], 3000) / 3000 * 0.5))
with open('blogs/final.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;'))
out = ['<?xml version="1.0" encoding="UTF-8"?>', '<opml version="2.0">', '  <head>',
       '    <title>HN Independent Blog Index</title>',
       '    <dateCreated>Mon, 03 Nov 2026 11:55:00 +0800</dateCreated>', '  </head>', '  <body>']
for cat in ('个人博客', '团队/工程博客'):
    out.append(f'    <outline text="{cat}" title="{cat}">')
    for r in rows:
        if r['category'] != cat: continue
        t = f"{r['domain']} · {r['posts']}篇 · avg {r['avg_score']:.0f} · {r['first']}-{r['last']}"
        out.append(f'      <outline type="rss" text="{esc(t)}" title="{esc(r["domain"])}" '
                   f'xmlUrl="{esc(r["feed"])}" htmlUrl="https://{esc(r["domain"])}"/>')
    out.append('    </outline>')
out += ['  </body>', '</opml>']
open('blogs/hn-blogs.opml', 'w').write("\n".join(out))
print("blogs:", len(rows), collections.Counter(r['category'] for r in rows))
