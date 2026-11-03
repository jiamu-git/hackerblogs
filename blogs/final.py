"""Curate final blog list, emit OPML + CSV."""
import json, csv

PERSONAL = set("""
chris-granger.com lofibucket.com antirez.com neilwithdata.com kalzumeus.com
jacquesmattheij.com candyjapan.com righto.com troyhunt.com adriancourreges.com
caseyliss.com mattkeeter.com robertxiao.ca phoboslab.org anishathalye.com
roguelazer.com saminiir.com paulgraham.com bitlog.com darkcoding.net
fabiensanglard.net bti360.com stavros.io ontestautomation.com bunniestudios.com
pushing-pixels.org bryanbraun.com ekioh.com geoffreylitt.com sandimetz.com
a1k0n.net stallman.org bzarg.com malwaretech.com jbkempf.com grumpygamer.com
adayinthelifeof.nl copetti.org downtowndougbrown.com chrisfenton.com csun.io
idlewords.com patrick-breyer.de dzombak.com ybrikman.com benkuhn.net
brandons.me dkriesel.com evanmiller.org agwa.name earslap.com drewdevault.com
redblobgames.com jordanmechner.com webworm.co hillelwayne.com gaudi.ch
projectgus.com robinsloan.com baekdal.com marco.org ctrl.blog bitquabit.com
gabrielweinberg.com nycresistor.com keacher.com nycmesh.net filfre.net
e-basteln.de aerogrammestudio.com linusakesson.net catonmat.net
imperialviolet.org jefftk.com hogbaysoftware.com happyassassin.net
anfractuosity.com electrospaces.net craigkerstiens.com joshwcomeau.com
tnhh.net pcmaffey.com talkingquickly.co.uk masteringemacs.org kennethreitz.org
bigmessowires.com somebits.com gregegan.net jacobian.org krebsonsecurity.com
scattered-thoughts.net jeremykun.com realworldtech.com revk.uk matuzo.at
danshapiro.com pathsensitive.com ctrl-alt-test.fr eevblog.com adit.io
gautamnarula.com stevenbuccini.com baldurbjarnason.com thanassis.space
scottrlarson.com noulakaz.net ethanhein.com engineersneedart.com dannyguo.com
5snb.club codeofhonor.com robertxiao.ca kim... 
""".split()) - {"kim..."}

TEAM = set("""
signal.org cockroachlabs.com inkandswitch.com igalia.com edgedb.com
volexity.com instantdb.com elysian.press fast.ai
""".split())

def main():
    probe = {x['domain']: x.get('feed') for x in json.load(open('blogs/probe_result.json'))}
    cand = {r['domain']: r for r in csv.DictReader(open('blogs/candidates.csv'))}
    rows = []
    for d in sorted(PERSONAL | TEAM):
        if d not in probe:
            print("MISSING from probe:", d); continue
        if not probe[d]:
            print("no feed:", d); continue
        r = cand[d]
        rows.append({'domain': d, 'feed': probe[d],
                     'category': '个人博客' if d in PERSONAL else '团队/工程博客',
                     'posts': int(r['sub_n']), 'avg_score': float(r['avg']),
                     'years': int(r['yrs']), 'first': r['first'], 'last': r['last'],
                     'mentions': int(r['cmt'])})
    rows.sort(key=lambda r: (-r['avg_score'] * (1 + r['years'] / 10)))
    with open('blogs/final.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"final blogs: {len(rows)}")

    def esc(s):
        return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                 .replace('"', '&quot;'))
    out = ['<?xml version="1.0" encoding="UTF-8"?>', '<opml version="2.0">',
           '  <head>',
           '    <title>HN Independent Blog Index</title>',
           '    <dateCreated>Mon, 03 Nov 2026 11:40:00 +0800</dateCreated>',
           '    <ownerName>HN 20-year archive mining</ownerName>',
           '  </head>', '  <body>']
    for cat in ('个人博客', '团队/工程博客'):
        out.append(f'    <outline text="{esc(cat)}" title="{esc(cat)}">')
        for r in rows:
            if r['category'] != cat: continue
            t = f"{r['domain']} · {r['posts']}篇 · avg {r['avg_score']:.0f} · {r['first']}-{r['last']}"
            out.append(f'      <outline type="rss" text="{esc(t)}" title="{esc(r["domain"])}" '
                       f'xmlUrl="{esc(r["feed"])}" htmlUrl="https://{esc(r["domain"])}"/>')
        out.append('    </outline>')
    out += ['  </body>', '</opml>']
    open('blogs/hn-blogs.opml', 'w').write("\n".join(out))
    print("wrote OPML")
    # category counts
    import collections
    print(collections.Counter(r['category'] for r in rows))

if __name__ == '__main__':
    main()
