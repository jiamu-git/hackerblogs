import csv, math, sys
import duckdb
sys.path.insert(0,'blogs')
from classify import is_blog

final = {r['domain'] for r in csv.DictReader(open('blogs/final.csv'))}
con = duckdb.connect(); con.execute("SET threads=4")
rows = con.execute("""SELECT url, host, title, sub_years, sub_n, best_score, cmt_n, cmt_years, years
                      FROM 'blogs/post_canon.parquet' WHERE url IS NOT NULL""").fetchall()
JUNK = {'example.com','localhost','127.0.0.1','xkcd.com','t.co','bit.ly','ow.ly'}

def norm(h):
    h = (h or '').lower()
    return h[4:] if h.startswith('www.') else h

def build(pred):
    out=[]
    for url,host,title,sy,sn,bs,cn,cy,years in rows:
        h=norm(host)
        if not h or h in JUNK or not pred(h): continue
        path = url.split('/', 3)[3] if url.count('/') >= 3 else ''
        if path in ('', '/') or len(path) < 3: continue   # skip homepages
        if any(x in url for x in ('index.html','/index.php','/blog/','/blog"')): pass
        score = years*3 + min(math.log10(1+(cn or 0)),3)*4 + min((bs or 0)/150,3)
        out.append({'url':url,'host':h,'title':title or '','years':int(years),
                    'sub_n':int(sn or 0),'cmt_n':int(cn or 0),'best':int(bs or 0),
                    'score':round(score,2)})
    out.sort(key=lambda r:-r['score'])
    return out

blog = build(lambda h: h in final)
glob = build(lambda h: is_blog(h)[0])

def cap3(items,n=40):
    seen={}; res=[]; keys=set()
    for r in items:
        path = r['url'].split('/',3)[3] if r['url'].count('/')>=3 else ''
        k=(r['host'], path.rstrip('/').lower())
        if k in keys: continue
        keys.add(k)
        if seen.get(r['host'],0)>=3: continue
        seen[r['host']]=seen.get(r['host'],0)+1
        res.append(r)
        if len(res)>=n: break
    return res

blog_c, glob_c = cap3(blog,45), cap3(glob,45)
for name,data in (('posts_from_list',blog),('posts_global',glob),
                  ('top_from_list',blog_c),('top_global',glob_c)):
    with open(f'blogs/{name}.csv','w',newline='') as fh:
        w=csv.DictWriter(fh,fieldnames=list(data[0].keys())); w.writeheader(); w.writerows(data)
print("=== 来自 120 个博客的反复引用文章 (top 30, 每站≤3) ===")
for r in blog_c[:30]:
    print(f"{r['years']:2d}y {r['cmt_n']:5d}m {r['best']:4d}p | {r['host']:26s} | {r['title'][:64] or r['url'][:64]}")
print("\n=== 全库范围 (top 20, 每站≤3) ===")
for r in glob_c[:20]:
    print(f"{r['years']:2d}y {r['cmt_n']:5d}m {r['best']:4d}p | {r['host']:26s} | {r['title'][:64] or r['url'][:64]}")
