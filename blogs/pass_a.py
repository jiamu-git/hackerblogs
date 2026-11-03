"""Pass A: per-domain stats from story submissions."""
import glob, json, re, collections
import pyarrow.parquet as pq

stats = {}
def domain(u):
    m = re.match(r'https?://([^/]+)', u or '')
    if not m: return None
    d = m.group(1).lower().split(':')[0]
    return d[4:] if d.startswith('www.') else d

files = sorted(glob.glob('hacker-news/data/*/*.parquet'))
for n, f in enumerate(files, 1):
    t = pq.read_table(f, columns=['type', 'url', 'score', 'time'])
    ty = t.column('type').to_pylist()
    urls = t.column('url').to_pylist()
    scores = t.column('score').to_pylist()
    times = t.column('time').to_pylist()
    for i, tyv in enumerate(ty):
        if tyv != 1: continue
        d = domain(urls[i])
        if not d: continue
        sc = scores[i] or 0
        yr = times[i].year
        s = stats.get(d)
        if s is None:
            s = stats[d] = {'n': 0, 'sum': 0, 'max': 0, 'hi': 0, 'years': set(), 'recent': 0}
        s['n'] += 1
        s['sum'] += sc
        if sc > s['max']: s['max'] = sc
        if sc >= 100: s['hi'] += 1
        s['years'].add(yr)
        if yr >= 2024: s['recent'] += 1
    if n % 40 == 0:
        print(f"{n}/{len(files)}  domains={len(stats)}", flush=True)

out = {}
for d, s in stats.items():
    out[d] = {'n': s['n'], 'avg': round(s['sum'] / s['n'], 1), 'max': s['max'],
              'hi': s['hi'], 'years': sorted(s['years']), 'nyears': len(s['years']),
              'recent': s['recent'], 'first': min(s['years']), 'last': max(s['years'])}
json.dump(out, open('blogs/domains.json', 'w'))
print("domains:", len(out))
