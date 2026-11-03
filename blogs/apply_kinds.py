"""Apply content classification, add a one-line intro per site."""
import csv, json, re, sys, collections
sys.path.insert(0, 'blogs')

# corrections from reading the top 150 by hand
EXTRA_PRODUCT = set("""
blitzortung.org thomask.sdf.org xiph.org training.kalzumeus.com
nvidia.github.io eugene.kaspersky.com margin.re suckless.org tldp.org
readyset.io computationalculture.net humbledollar.com airliners.net muted.io
gameworldobserver.com arclanguage.org
""".split())

BOILER = re.compile(r'(cookie|javascript is|enable js|official (site|website)|welcome to my'
                    r'|just another|powered by|best viewed)', re.I)

def clean_intro(s):
    s = re.sub(r'\s+', ' ', s or '').strip(' -|·')
    s = s.replace('&#x27;', "'").replace('&#39;', "'").replace('&amp;', '&')
    s = re.sub(r'&#?\w+;', '', s)
    return s

def make_desc(meta):
    desc = clean_intro(meta.get('desc', ''))
    if 25 <= len(desc) <= 150 and not BOILER.search(desc):
        return desc
    return ''

def main():
    kinds = json.load(open('blogs/kinds.json'))
    meta = {m['d']: m for m in json.load(open('/tmp/allmeta.json'))}
    rows = list(csv.DictReader(open('blogs/final.csv')))
    out = []
    for r in rows:
        d = r['domain']
        k = kinds.get(d, {}).get('kind', 'company')
        if d in EXTRA_PRODUCT:
            k = 'product'
        if k == 'product':
            continue
        r['kind'] = 'blog' if k == 'blog' else 'company'
        r['desc'] = make_desc(meta.get(d, {}))
        out.append(r)
    with open('blogs/final.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
        w.writeheader(); w.writerows(out)
    from curate import write_opml
    feed_rows = [r for r in out if r['kind'] == 'blog']
    write_opml(feed_rows)
    write_opml(feed_rows, 'blogs/hn-blogs-top300.opml', top=300)
    print(collections.Counter(r['kind'] for r in out), len(out))

if __name__ == '__main__':
    main()
