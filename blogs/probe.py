"""Discover RSS/Atom feed for candidate blog domains."""
import csv, json, re, sys, concurrent.futures as cf
import urllib.request, urllib.error, socket

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
COMMON = ["/feed", "/rss", "/rss.xml", "/atom.xml", "/feed.xml", "/index.xml"]
LINK_RE = re.compile(
    r'<link[^>]+(?:type=["\']application/(?:rss|atom)\+xml["\'][^>]*href=["\']([^"\']+)["\']'
    r'|href=["\']([^"\']+)["\'][^>]*type=["\']application/(?:rss|atom)\+xml["\'])', re.I)
TITLE_RE = re.compile(r'<title[^>]*>(.*?)</title>', re.S | re.I)

def fetch(url, timeout=4, maxbytes=300_000):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read(maxbytes)
        return r.geturl(), r.headers.get("Content-Type", ""), data

def is_feed(ct, body):
    if any(x in ct for x in ("rss", "atom", "xml")):
        head = body[:2000].lower()
        if b"<rss" in head or b"<feed" in head or b"<rdf" in head:
            return True
    head = body[:2000].lower()
    return b"<rss" in head or b"<atom" in head

def domain_feed(domain):
    base = f"https://{domain}"
    # 1) homepage autodiscovery
    try:
        final, ct, body = fetch(base + "/")
        m = LINK_RE.search(body.decode("utf-8", "ignore"))
        if m:
            href = (m.group(1) or m.group(2)).strip()
            if href.startswith("//"): href = "https:" + href
            elif href.startswith("/"): href = base + href
            elif not href.startswith("http"): href = base + "/" + href
            try:
                f2, ct2, b2 = fetch(href)
                if is_feed(ct2, b2):
                    return {"feed": f2, "how": "autodiscover"}
            except Exception:
                pass
    except Exception:
        pass
    # 2) common paths
    for p in COMMON:
        try:
            u, ct, b = fetch(base + p)
            if is_feed(ct, b):
                return {"feed": u, "how": "common" + p}
        except Exception:
            continue
    return None

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    rows = list(csv.DictReader(open("blogs/candidates.csv")))[:n]
    out = []
    def work(r):
        d = r["domain"]
        try:
            res = domain_feed(d)
        except Exception as e:
            res = None
        if res:
            res["domain"] = d
            return res
        return {"domain": d, "feed": None}
    with cf.ThreadPoolExecutor(40) as ex:
        for i, r in enumerate(ex.map(work, rows), 1):
            out.append(r)
            if i % 10 == 0:
                ok = sum(1 for x in out if x["feed"])
                print(f"{i}/{len(rows)} feeds={ok}", flush=True)
    json.dump(out, open("blogs/probe_result.json", "w"))
    ok = [x for x in out if x["feed"]]
    print(f"done: {len(ok)}/{len(out)} feeds found")
    for x in ok[:15]:
        print(" ", x["domain"], "->", x["feed"][:80], x["how"])

if __name__ == "__main__":
    socket.setdefaulttimeout(8)
    main()
