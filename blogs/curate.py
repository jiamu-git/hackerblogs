"""Curate the catalog: drop product/project sites, tag company blogs.

Two mechanisms:
  1. structural: submissions dominated by the root path, or by download /
     changelog / docs paths, mean the site is a product, not a blog.
  2. explicit: hand-reviewed domains from the top of the ranking, where
     structure cannot separate a company blog from a personal one.
"""
import csv, json, re, duckdb
import sys
sys.path.insert(0, 'blogs')
from verdicts import CONTENT_DROP, CONTENT_COMPANY

PRODUCT = set("""
pandoc.org iterm2.com windows93.net justgetflux.com starlink.com system76.com
ipfs.io elm-lang.org kerbalspaceprogram.com krita.org releases.ubuntu.com
spacex.com blockchain.com sagemath.org play0ad.com mersenne.org pharo.org
fishshell.com dynamicland.org passwordstore.org syncthing.net sqlite.org
android.googlesource.com nixos.org ruby-lang.org craftinginterpreters.com
quilljs.com explainshell.com regexper.com calculusmadeeasy.org ghostty.org
mycroft.ai musclewiki.com 507movements.com streaming.media.ccc.de wikihouse.cc
pointerpointer.com adventofcode.com icq.com asciiflow.com
how-i-experience-web-today.com orgmode.org openwrt.org chromium.googlesource.com
course.fast.ai doc.rust-lang.org linuxfromscratch.org bitcoin.org
lists.torproject.org nand2tetris.org kolibrios.org littleosbook.github.io
jellyfin.org asahilinux.org remarkable.com qwenlm.github.io bay12games.com
jdk.java.net racket-lang.org librivox.org libcello.org algorithmsbook.com
weavesilk.com sifive.com graalvm.org duckduckgo.com serenityos.org tosdr.org
3blue1brown.com seat61.com echarts.apache.org ziglang.org learntla.com
mailarchive.ietf.org helix-editor.com bethesda.net coffeescript.org
boringcompany.com gobolinux.org bottomupcs.com pgexercises.com untools.co
blot.im ssh.com plumshell.com openssl.org braveclojure.com elixir-lang.org
home-assistant.io raspberrypi.org blender.org gimp.org videolan.org
mono-project.com phoenixframework.org rethinkdb.com openra.net gnucash.org
beagleboard.org hammerspoon.org pine64.org factorio.com darktable.org
keycloak.org vogons.org haiku-os.org erlang.org xfce.org blackmagicdesign.com
jenkins.io midi.org openttd.org reactos.org qemu.org fossil-scm.org xlwings.org
obdev.at mailgun.com open-emr.org standardebooks.org calibre-ebook.com
protondb.com smartcar.com interdb.jp obsproject.com parceljs.org brew.sh
stockfishchess.org rebble.io mitmproxy.org pi-hole.net notepad-plus-plus.org
obsidian.md restic.net sailfishos.org sandstorm.io stellarium.org tokio.rs
veloren.net zed.dev capnproto.org deno.land devdocs.io f-droid.org httpie.io
jitsi.org julialang.org letsencrypt.org libera.chat lineageos.org litestream.io
matrix.org mistral.ai mullvad.net netboot.xyz nim-lang.org pidgin.im
plausible.io astral.sh bevyengine.org
""".split())

ORG_TLD = ('.gov', '.gov.uk', '.edu', '.ac.uk', '.mil', '.int', '.eu', '.org.uk')
ORG_WORDS = ('foundation', 'alliance', 'institute', 'association', 'consortium',
             'society', 'council', 'agency', 'bureau', 'ministry', 'university',
             'college', 'laboratory', 'foundation', 'initiative')

COMPANY = set("""
signal.org stripe.com cockroachlabs.com jepsen.io smallstep.com backblaze.com
ccc.de media.ccc.de fidoalliance.org gds.blog.gov.uk framablog.org nycresistor.com
tailscale.com fly.io github.blog blog.cloudflare.com cloudflare.com
openai.com anthropic.com figma.com vercel.com netlify.com docker.com
hashicorp.com mongodb.com redis.io postgresql.org mysql.com
""".split())

PROD_RE = re.compile(r'^/(download|downloads|changelog|releases?|pricing|install'
                     r'|store|product)(/|$)', re.I)

def structural(rows):
    """rows: (domain, url) pairs. Returns {domain: (n, root_frac, prod_frac)}."""
    from collections import defaultdict
    agg = defaultdict(lambda: [0, 0, 0])
    for d, u in rows:
        a = agg[d]
        a[0] += 1
        path = u.split('/', 3)[3] if u.count('/') >= 3 else ''
        if path.strip('/') == '':
            a[1] += 1
        if PROD_RE.search('/' + path):
            a[2] += 1
    return {d: (n, r / n, p / n) for d, (n, r, p) in agg.items()}

def esc(s):
    return (s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def write_opml(rows, path='blogs/hn-blogs.opml', top=None):
    """Flat OPML: no groups, so no duplicate entries after import."""
    seen, feed_rows = set(), []
    for r in rows:
        u = (r.get('feed') or '').strip()
        if not u or u in seen:
            continue
        seen.add(u)
        feed_rows.append(r)
    if top:
        feed_rows = feed_rows[:top]
    out = ['<?xml version="1.0" encoding="UTF-8"?>', '<opml version="2.0">', '  <head>',
           '    <title>HN Independent Blog Index</title>',
           f'    <dateCreated>{__import__("email.utils", fromlist=["formatdate"]).formatdate(localtime=True)}</dateCreated>',
           '  </head>', '  <body>']
    for r in feed_rows:
        t = f"{r['domain']} · {r['posts']} posts · p90 {r['p90']} · {r['first']}-{r['last']}"
        out.append(f'    <outline type="rss" text="{esc(t)}" title="{esc(r["domain"])}" '
                   f'xmlUrl="{esc(r["feed"])}" htmlUrl="https://{esc(r["domain"])}"/>')
    out += ['  </body>', '</opml>']
    open(path, 'w').write("\n".join(out))
    print(f"{path}: {len(feed_rows)} feeds")

def main():
    con = duckdb.connect(); con.execute("SET threads=4")
    rows = con.execute("""SELECT lower(regexp_replace(host,'^www\\.','')) d, url
                          FROM 'blogs/story_urls.parquet'""").fetchall()
    st = structural(rows)

    final = list(csv.DictReader(open('blogs/final.csv')))
    kept, dropped = [], {"product": 0, "structural": 0}
    for r in final:
        d = r['domain']
        n, root, prod = st.get(d, (0, 0, 0))
        if d in PRODUCT or d in CONTENT_DROP:
            dropped["product"] += 1
            continue
        if n >= 6 and (root >= 0.30 or prod >= 0.25):
            dropped["structural"] += 1
            continue
        is_org = (d in COMPANY or d in CONTENT_COMPANY or d.endswith(ORG_TLD)
                  or any(w in d for w in ORG_WORDS))
        r['kind'] = 'company' if is_org else 'personal'
        kept.append(r)

    with open('blogs/final.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(kept[0].keys()))
        w.writeheader(); w.writerows(kept)

    write_opml(kept)
    write_opml(kept, 'blogs/hn-blogs-top300.opml', top=300)
    import collections
    print(f"kept={len(kept)} dropped={dropped} kinds={collections.Counter(r['kind'] for r in kept)}")
    print("\ntop 25 after curation:")
    for r in kept[:25]:
        print(f"  {float(r['score']):6.0f} {r['domain']:32s} {r['kind']:9s} {r['posts']:>4} posts")

if __name__ == '__main__':
    main()
