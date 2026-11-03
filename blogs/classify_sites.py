"""Classify every catalogued site from its content sample.

  blog     writing-first site with positive evidence; kept in the main list
  company  organisation, company, project or forum; tagged, hidden by default
  product  product, tool, store, docs or archive; dropped

Precision over recall: a site needs positive evidence to be called a blog.
Anything unverified leaves the main list and is reported as such.
"""
import json, re, sys, collections
import duckdb
sys.path.insert(0, 'blogs')
from verdicts import CONTENT_DROP, CONTENT_COMPANY

VER = re.compile(r'\b(v|version\s*)?\d+\.\d+(\.\d+)?\b|\breleased?\b|\brelease notes\b'
                 r'|\bchangelog\b|\bnow available\b', re.I)
# phrases that only a product or a vendor writes
PRODUCT = re.compile(r'\b(download now|pricing|free trial|sign ?up|get started|book a demo'
                     r'|add to cart|buy now|our (platform|product|app)|the world\'s (first|best)'
                     r'|enterprise (platform|software|solution)|cloud hosting|web hosting'
                     r'|domain names?|vpn|antivirus|password manager|api for)\b', re.I)
ORG = re.compile(r'\b(foundation|institute|alliance|association|council|consortium'
                 r'|university|department of|school of|college|laborator(y|ies)|non-?profit'
                 r'|mailing list|mailman|phabricator|inc\.|ltd\.?|gmbh|corp\.)\b', re.I)
MEDIA = re.compile(r'\b(news|magazine|journal|daily|weekly|herald|tribune|gazette'
                   r'|breaking news|press release|tv station|radio station'
                   r'|stock exchange|market data)\b', re.I)
FORUM = re.compile(r'\b(forum|forums|message board|discussion board|community site'
                   r'|stack exchange|mailing list archive)\b', re.I)
BLOG = re.compile(r'\b(blog|weblog|notes|essays|writings|thoughts|articles|journal of)\b', re.I)
VERDICT_KEEP = {'signal.org','jepsen.io','danluu.com','gwern.net'}

def hn_titles():
    con = duckdb.connect()
    rows = con.execute("""
      WITH t AS (
        SELECT lower(regexp_replace(host,'^www\\.','')) d, title, score,
               row_number() OVER (PARTITION BY lower(regexp_replace(host,'^www\\.',''))
                                  ORDER BY score DESC) rn
        FROM 'blogs/story_urls.parquet' WHERE title IS NOT NULL AND length(title) > 12
      )
      SELECT d, title FROM t WHERE rn <= 12
    """).fetchall()
    out = collections.defaultdict(list)
    for d, t in rows:
        out[d].append(t)
    return out

TITLES = hn_titles()

def blog_evidence(meta):
    """Return a reason string if the site looks like writing-first, else ''."""
    items = meta.get('items') or TITLES.get(meta['d'], [])
    title = meta.get('title') or meta.get('feed_title') or ''
    desc = meta.get('desc') or ''
    if len(items) >= 3:
        rel = sum(1 for t in items[:10] if VER.search(t)) / len(items[:10])
        words = sorted(len(t.split()) for t in items[:10])
        med = words[len(words) // 2]
        if rel < 0.3 and med >= 3:
            return f'feed of {len(items)} posts, {rel:.0%} releases'
    if BLOG.search(title + ' ' + desc) and len(title + desc) > 15:
        return 'blog wording on the page'
    return ''

def classify(meta):
    d = meta['d']
    items = meta.get('items') or []
    title = meta.get('title') or meta.get('feed_title') or ''
    desc = meta.get('desc') or ''
    page = f'{title} {desc}'.strip()

    if d in CONTENT_DROP:
        return 'product', 'hand-reviewed: product or project'
    if d in CONTENT_COMPANY:
        return 'company', 'hand-reviewed: company or organisation'

    if any(x in d for x in ('.gov', '.edu', '.ac.uk', '.mil')):
        return 'company', 'institutional domain'
    if ORG.search(page):
        return 'company', 'organisation wording on the page'
    if FORUM.search(page):
        return 'company', 'forum or community wording'
    if MEDIA.search(page):
        return 'product', 'news or media outlet'
    if PRODUCT.search(page):
        return 'product', 'vendor wording on the page'

    rel = (sum(1 for t in items[:10] if VER.search(t)) / len(items[:10])) if items else 0
    if items and rel >= 0.5:
        return 'product', f'release notes feed ({rel:.0%} of items)'

    ev = blog_evidence(meta)
    if ev:
        return 'blog', ev
    if d in VERDICT_KEEP:
        return 'blog', 'hand-reviewed'
    return 'company', 'no positive evidence of writing'

def main():
    metas = json.load(open('/tmp/allmeta.json'))
    out = {m['d']: dict(zip(('kind', 'why'), classify(m))) for m in metas}
    json.dump(out, open('blogs/kinds.json', 'w'))
    print(collections.Counter(v['kind'] for v in out.values()))
    for r, n in collections.Counter(v['why'].split('(')[0].split(':')[0].strip()
                                    for v in out.values()).most_common(10):
        print(f'  {n:5d}  {r}')

if __name__ == '__main__':
    main()
