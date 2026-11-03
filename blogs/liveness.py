"""One request per domain: is it reachable, and does its HTML advertise a feed?"""
import csv, json, re, socket, sys, time
import concurrent.futures as cf
import urllib.request, urllib.error, ssl

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
LINK_RE = re.compile(
    r'<link[^>]+(?:type=["\']application/(?:rss|atom)\+xml["\'][^>]*href=["\']([^"\']+)["\']'
    r'|href=["\']([^"\']+)["\'][^>]*type=["\']application/(?:rss|atom)\+xml["\'])', re.I)
TITLE_RE = re.compile(r'<title[^>]*>(.*?)</title>', re.S | re.I)
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

def probe(domain):
    rec = {"domain": domain, "ok": False, "status": None, "feed": None,
           "title": None, "final": None, "err": None, "ms": None}
    t0 = time.time()
    for scheme in ("https", "http"):
        url = f"{scheme}://{domain}/"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
            with urllib.request.urlopen(req, timeout=5, context=CTX) as r:
                body = r.read(300_000)
                rec["status"] = r.status
                rec["final"] = r.geturl()
                rec["ok"] = True
                html = body.decode("utf-8", "ignore")
                m = LINK_RE.search(html)
                if m:
                    href = (m.group(1) or m.group(2)).strip()
                    base = f"{scheme}://{domain}"
                    if href.startswith("//"): href = "https:" + href
                    elif href.startswith("/"): href = base + href
                    elif not href.startswith("http"): href = base + "/" + href
                    rec["feed"] = href
                t = TITLE_RE.search(html)
                if t:
                    rec["title"] = re.sub(r"\s+", " ", t.group(1)).strip()[:120]
                break
        except urllib.error.HTTPError as e:
            rec["status"] = e.code
            if e.code and e.code < 500:
                rec["err"] = f"http_{e.code}"; break
            rec["err"] = f"http_{e.code}"
        except urllib.error.URLError as e:
            rec["err"] = f"url:{str(e.reason)[:40]}"
        except socket.timeout:
            rec["err"] = "timeout"
        except Exception as e:
            rec["err"] = type(e).__name__
    rec["ms"] = int((time.time() - t0) * 1000)
    return rec

def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    rows = list(csv.DictReader(open("blogs/candidates.csv")))
    if limit: rows = rows[:limit]
    out, t0 = [], time.time()
    with cf.ThreadPoolExecutor(80) as ex:
        for i, rec in enumerate(ex.map(probe, [r["domain"] for r in rows]), 1):
            out.append(rec)
            if i % 500 == 0:
                ok = sum(1 for x in out if x["ok"])
                fd = sum(1 for x in out if x["feed"])
                print(f"{i}/{len(rows)} ok={ok} ({ok/i*100:.0f}%) feed={fd} ({fd/i*100:.0f}%) {time.time()-t0:.0f}s", flush=True)
    json.dump(out, open("blogs/liveness.json", "w"))
    ok = [x for x in out if x["ok"]]
    print(f"done: {len(out)} probed, {len(ok)} reachable, {sum(1 for x in ok if x['feed'])} with feed")

if __name__ == "__main__":
    socket.setdefaulttimeout(6)
    main()
