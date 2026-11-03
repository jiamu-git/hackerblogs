"""Domain classification for the HN independent-blog census.

Keep = personal / small-team blogs, technical write-ups, long-form essays.
Drop = news media, UGC platforms, docs/wiki, commerce, SEO farms, Q&A.
"""

MEDIA = {
    "nytimes.com", "wsj.com", "bloomberg.com", "reuters.com", "theguardian.com",
    "bbc.com", "bbc.co.uk", "cnn.com", "washingtonpost.com", "theverge.com",
    "techcrunch.com", "arstechnica.com", "wired.com", "theregister.com",
    "theregister.co.uk", "economist.com", "ft.com", "forbes.com",
    "businessinsider.com", "cnbc.com", "npr.org", "theatlantic.com",
    "newyorker.com", "qz.com", "engadget.com", "gizmodo.com", "mashable.com",
    "thenextweb.com", "venturebeat.com", "zdnet.com", "technologyreview.com",
    "spectrum.ieee.org", "phys.org", "nature.com", "sciencemag.org", "science.org",
    "cnet.com", "slate.com", "vox.com", "axios.com", "politico.com",
    "huffingtonpost.com", "huffpost.com", "vice.com", "motherboard.vice.com",
    "theintercept.com", "propublica.org", "apnews.com", "latimes.com",
    "usatoday.com", "time.com", "newsweek.com", "thehill.com", "wired.co.uk",
    "newstatesman.com", "independent.co.uk", "telegraph.co.uk", "spiegel.de",
    "lemonde.fr", "nikkei.com", "scmp.com", "aljazeera.com", "abc.net.au",
    "cbc.ca", "globeandmail.com", "nationalpost.com", "smh.com.au",
    "theinformation.com", "semianalysis.com", "stratechery.com", "platformer.news",
    "arstechnica.co.uk", "extremetech.com", "tomshardware.com", "anandtech.com",
    "the-decoder.com", "techmeme.com", "slashdot.org", "businessinsider.nl",
    "inc.com", "fastcompany.com", "fortune.com", "hbr.org", "mit.edu",
    "technologyreview.com", "scientificamerican.com", "newscientist.com",
    "quantamagazine.org", "nautil.us", "aeon.co", "lrb.co.uk", "nybooks.com",
    "thebrowser.com", "worksinprogress.co", "asteriskmag.com", "palladiummag.com",
}

PLATFORM = {
    "youtube.com", "youtu.be", "twitter.com", "x.com", "reddit.com",
    "old.reddit.com", "linkedin.com", "facebook.com", "instagram.com",
    "medium.com", "github.com", "gist.github.com", "stackoverflow.com",
    "stackexchange.com", "news.ycombinator.com", "google.com", "goo.gl",
    "wikipedia.org", "en.wikipedia.org", "arxiv.org", "ssrn.com",
    "researchgate.net", "academia.edu", "quora.com", "producthunt.com",
    "crunchbase.com", "docs.google.com", "sites.google.com", "drive.google.com",
    "dropbox.com", "imgur.com", "flickr.com", "vimeo.com", "soundcloud.com",
    "spotify.com", "apple.com", "amazon.com", "ebay.com", "patreon.com",
    "kickstarter.com", "indiegogo.com", "gofundme.com", "dev.to",
    "hackernoon.com", "dzone.com", "towardsdatascience.com",
    "betterprogramming.pub", "levelup.gitconnected.com", "hashnode.com",
    "substack.com", "ghost.io", "wordpress.com", "blogspot.com", "tumblr.com",
    "pinterest.com", "tiktok.com", "twitch.tv", "discord.com", "slack.com",
    "notion.so", "figma.com", "zoom.us", "telegra.ph", "pastebin.com",
    "archive.org", "web.archive.org", "doi.org", "sci-hub.se",
    "ieee.org", "acm.org", "springer.com", "sciencedirect.com", "wiley.com",
    "tandfonline.com", "cambridge.org", "oup.com", "jstor.org", "plos.org",
    "biorxiv.org", "medrxiv.org", "papers.ssrn.com", "nber.org", "rand.org",
    "brookings.edu", "pewresearch.org", "statista.com", "ourworldindata.org",
    "bls.gov", "census.gov", "nih.gov", "cdc.gov", "who.int", "un.org",
    "europa.eu", "gov.uk", "whitehouse.gov", "congress.gov", "supremecourt.gov",
    "courtlistener.com", "law.cornell.edu", "justia.com", "scholar.google.com",
    "books.google.com", "goodreads.com", "amazon.co.uk", "audible.com",
    "nytimes.com", "wsj.com", "ft.com", "economist.com", "bloomberg.com",
}

# prefixes that mean "corporate site / docs / shop", not an independent blog
DROP_PREFIXES = (
    "docs.", "developer.", "developers.", "learn.", "support.", "help.",
    "wiki.", "forum.", "community.", "discuss.", "news.", "blog.google",
    "store.", "apps.", "play.", "itunes.", "market.", "shop.", "status.",
    "careers.", "jobs.", "investor.", "investors.", "press.", "legal.",
    "policies.", "cloud.", "console.", "admin.", "api.", "cdn.", "static.",
    "assets.", "download.", "downloads.", "get.", "try.", "go.", "my.",
)

DROP_SUFFIX_HINTS = (
    "github.io",  # NO: many great personal blogs live here -> handled below
)


def is_blog(domain: str) -> tuple[bool, str]:
    """Return (keep, reason)."""
    d = domain.lower()
    if not d or "." not in d:
        return False, "invalid"
    if d in MEDIA:
        return False, "media"
    if d in PLATFORM:
        return False, "platform"
    if d.startswith(DROP_PREFIXES):
        return False, "prefix"
    if d.endswith((".gov", ".mil", ".edu")):
        return False, "institution"
    if any(x in d for x in ("cdnpkg", "cloudfront", "amazonaws", "herokuapp")):
        return False, "hosting"
    return True, "candidate"


# Domains that are technically company/org sites but read like blogs and are
# widely subscribed to as such. Tagged separately, still included.
ORG_BLOGS = {
    "jepsen.io", "signal.org", "tailscale.com", "fly.io", "danluu.com",
    "sqlite.org", "lwn.net", "nullprogram.com", "github.blog",
    "blog.cloudflare.com", "netflixtechblog.com", "engineering.fb.com",
    "increment.com", "stripe.com", "openai.com", "anthropic.com",
}

# Explicitly dropped from the blog list: software projects, institutions,
# news media, products, and reference sites. Everything else with a live
# feed is treated as a blog.
DROP = set("""
blender.org zotero.org ffmpeg.org sublimetext.com videolan.org mono-project.com
phoenixframework.org rethinkdb.com openra.net gnucash.org gimp.org
beagleboard.org cloudflarestatus.com hammerspoon.org pine64.org factorio.com
darktable.org home-assistant.io keycloak.org vogons.org haiku-os.org erlang.org
xfce.org blackmagicdesign.com raspberrypi.org jenkins.io midi.org openttd.org
openssl.org reactos.org qemu.org fossil-scm.org xlwings.org obdev.at lux.camera
mailgun.com open-emr.org nohello.com foldnfly.com animatedknots.com
openculture.com maps.org ecma-international.org wi-fi.org cnil.fr
nobelprize.org aclu.org eff.org gnu.org debian.org bmj.com nrk.no nrc.nl
aftenposten.no helsinkitimes.fi judiciary.uk cpj.org madinamerica.com
medialens.org pajiba.com chicagomaroon.com them.us eureporter.co statewatch.org
port.ac.uk ic.unicamp.br eso.org vibilagare.se forbrukerradet.no
iphoneincanada.ca bluewin.ch stephenfry.com terrybisson.com freerangekids.com
mitadmissions.org ccc.de sweethome3d.com wood-database.com githubstatus.com
icij.org privacyinternational.org bookstackapp.com oxfam.org
digitalcameraworld.com bluetooth.com usb.org ctan.org statnews.com
bicycling.com entsoe.eu mining.com audubon.org avweb.com penny-arcade.com
medievalists.net damninteresting.com askamathematician.com zompist.com
forth.com lua.org varnish-cache.org qubes-os.org ttnews.com fossjobs.net
fast.ai interdb.jp stimmel-law.com hudsandguis.com codeofhonor.com
standardebooks.org calibre-ebook.com protondb.com smartcar.com
search.marginalia.nu immersivemath.com monodraw.helftone.com intuitiveexplanations.com
ouroboros.org drakewest.com
""".split())

# Company / team engineering blogs (still worth subscribing, but not personal).
TEAM_EXTRA = set("""
signal.org cockroachlabs.com inkandswitch.com igalia.com edgedb.com
volexity.com instantdb.com elysian.press github.blog blog.cloudflare.com
jepsen.io tailscale.com fly.io stripe.com openai.com anthropic.com
danluu.com
""".split())

DROP |= set("""
astral.sh bevyengine.org brew.sh capnproto.org deno.land devdocs.io elixir-lang.org
f-droid.org httpie.io jitsi.org julialang.org letsencrypt.org libera.chat
lineageos.org litestream.io matrix.org mistral.ai mitmproxy.org mullvad.net
netboot.xyz nim-lang.org notepad-plus-plus.org obsidian.md obsproject.com
parceljs.org pi-hole.net pidgin.im plausible.io rebble.io restic.net
sailfishos.org sandstorm.io stockfishchess.org stellarium.org tokio.rs
veloren.net zed.dev blog.rust-lang.org blog.getbootstrap.com blog.jupyter.org
blog.mozilla.org hacks.mozilla.org blog.system76.com blog.archive.org
blog.newsblur.com blog.asciinema.org increase.com fly.io security.apple.com
brave.com wikimediafoundation.org sfwa.org fossi-foundation.org freedom.press
innocenceproject.org groundup.org.za thehub.ca thetech.com cgchannel.com
mothership.sg idw-online.de scilogs.spektrum.de thewaltdisneycompany.com
meta.slashdot.org metatalk.metafilter.com ooh.directory 1mb.club
musicforprogramming.net mynoise.net catandgirl.com csszengarden.com
floor796.com timetoplayfair.com reincubate.com deepsouthventures.com
every-layout.dev animatedengines.com beginners.re hscott.net
andrewducker.dreamwidth.org
""".split())

TEAM_EXTRA |= {"googleprojectzero.blogspot.com", "blog.pinboard.in", "blog.kagi.com",
               "citizenlab.ca"}
