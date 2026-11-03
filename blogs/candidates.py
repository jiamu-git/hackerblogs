"""Build the candidate list for RSS probing."""
import json, csv, sys, math
import duckdb
sys.path.insert(0,'blogs')
from classify import is_blog, ORG_BLOGS

dom = json.load(open('blogs/domains.json'))
con = duckdb.connect(); con.execute("SET threads=4")
cmt = {}
for h,n,y,u in con.execute("""SELECT lower(host), sum(n), count(DISTINCT yr), count(DISTINCT url)
    FROM 'blogs/comment_links.parquet' GROUP BY 1""").fetchall():
    h = h[4:] if h.startswith('www.') else h
    c = cmt.setdefault(h,[0,0,0]); c[0]+=n; c[1]=max(c[1],y); c[2]+=u
extra = {d:(u,r,y) for d,u,r,y in con.execute("SELECT * FROM 'blogs/domain_urls.parquet'").fetchall()}

rows=[]
for d,s in dom.items():
    if not is_blog(d)[0]: continue
    c = cmt.get(d,[0,0,0]); u,recent,_ = extra.get(d,(0,0,0))
    if s['n'] < 6 or s['nyears'] < 3: continue
    if u < 5: continue                      # needs real article pages
    if recent < 1 and s['last'] < 2023: continue   # must be alive
    q=min(s['avg'],400); p=min(s['nyears'],12)
    score = q*(0.4+p/12)*(1+min(math.log10(1+c[0]),3)/4) + min(recent,50)*0.5
    rows.append({'domain':d,'score':round(score,1),'sub_n':s['n'],'avg':s['avg'],'max':s['max'],
                 'yrs':s['nyears'],'first':s['first'],'last':s['last'],'urls':u,'recent':recent,
                 'cmt':c[0],'cmty':c[1],'org':d in ORG_BLOGS})
rows.sort(key=lambda r:-r['score'])
with open('blogs/candidates.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print("candidates:",len(rows))
for r in rows[:25]: print(f"  {r['score']:6.0f} {r['domain']:32s} n={r['sub_n']:4d} recent={r['recent']:3d} last={r['last']}")
