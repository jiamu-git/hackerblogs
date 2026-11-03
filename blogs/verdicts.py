"""Human verdicts from reading feed items and homepage text for the top 600.

CONTENT_DROP: product, company marketing, org, archive, parked, or redirect.
CONTENT_COMPANY: real blogs run by a company or foundation, kept but tagged.
Everything else in the top 600 stays personal.
"""

CONTENT_DROP = set("""
# languages, frameworks, runtimes
clojurescript.org crystal-lang.org tailwindcss.com blog.racket-lang.org blog.keras.io
rxdb.info nextjs.org django-rest-framework.org djangoproject.com typescriptlang.org
tensorflow.org pijul.org llvm.org blog.llvm.org nginx.org rocket.rs caddyserver.com
element.io thunderbird.net fastmail.com tarsnap.com virtualbox.org
fuchsia.dev fuchsia.googlesource.com
# project sites
libreboot.org nuitka.net blog.torproject.org dolphin-emu.org briarproject.org
blog.joinmastodon.org blog.elementary.io blog.gitbutler.com blog.zulip.com
cushionapp.com e.foundation ulisp.com greenteapress.com dragonflybsd.org
openbsd.org gcc.gnu.org tip.golang.org netflix.github.io microsoft.github.io
google.github.io
# mail archives and git hosts
lists.zx2c4.com lists.freebsd.org lists.webkit.org lists.gnu.org lists.w3.org
lists.wikimedia.org lists.torproject.org lists.squeakfoundation.org
mailman.nginx.org mailman.nanog.org marc.info lkml.org issues.apache.org
bugs.debian.org git.kernel.org phabricator.wikimedia.org seclists.org
# companies and products
pud.com copy.sh cses.fi digitalmars.com telegram.org kodak.com nintendo.co.jp
nintendo.co.uk analog.com adguard.com bitwarden.com draculatheme.com
1password.community starlabs.systems teenage.engineering logitech.com
minecraft.net disneyanimation.com lyft.com squareup.com waymo.com getcruise.com
boomsupersonic.com berkshirehathaway.com abc.xyz psl.com reaktor.com
tremendous.com pganalyze.com backblaze.com deepmind.com lexaloffle.com
exploringjs.com gameprogrammingpatterns.com minireference.com startupschool.org
readonlymemory.vg varasanos.com howacarworks.com austinmann.com
# org, government, education, media
wikileaks.org npl.co.uk comsec.ethz.ch ipp.mpg.de damtp.cam.ac.uk
cs.huji.ac.il comp.nus.edu.sg varsity.co.uk cable.co.uk who.is
find-and-update.company-information.service.gov.uk citizenlab.ca
ioccc.org erowid.org iism.org apmreports.org mainichi.jp bsky.social
grapheneos.social social.coop mamot.fr bittersoutherner.com avherald.com
harmful.cat-v.org genius.cat-v.org cheatsheetseries.owasp.org
# parked, moved, redirect
rednuht.org mfkl.github.io codersnotes.com aosabook.org bollu.github.io
google.github.io games.greggman.com
""".split())

CONTENT_DROP |= set("""
# second pass: shelf pool not covered by the top-600 review
ostif.org scummvm.org red-lang.org internals.rust-lang.org pola.rs blog.jquery.com
sourcehut.org home.cern blog.datomic.com idris-lang.org clojure.org blog.gtk.org
gfx-rs.github.io kernelnewbies.org bugs.ruby-lang.org htmx.org bits.debian.org
airbnb.io blog.dropbox.com distill.pub priceonomics.com cntraveler.com
nikonrumors.com cyclingweekly.com thelocal.dk governing.com finbold.com
2600.com lowtechmagazine.com x-plane.com rtl-sdr.com blurbusters.com
digiconomist.net inference.vc blog.fastforwardlabs.com positive.security
spreadprivacy.com mywiki.wooledge.org lwn.net people.xiph.org zachtronics.com
culture.pl panic.com qotoqot.com openrss.org foundersatwork.posthaven.com
compilers.iecc.com
""".split())

CONTENT_DROP |= set("""
techempower.com postgrespro.com gmunk.com lysator.liu.se solar.lowtechmagazine.com
250bpm.com howtomarketagame.com
""".split())

CONTENT_COMPANY = set("""
jepsen.io stripe.com smallstep.com cockroachlabs.com tailscale.com
blog.kagi.com blog.pinboard.in codewords.recurse.com bti360.com
signal.org ccc.de media.ccc.de fidoalliance.org gds.blog.gov.uk framablog.org igalia.com
nycresistor.com blog.racket-lang.org
""".split())

# feed items that are release notes rather than writing
RELEASE_SITES = set("""
clojurescript.org libreboot.org nuitka.net blog.torproject.org crystal-lang.org
dolphin-emu.org blog.zulip.com cushionapp.com e.foundation tailwindcss.com
briarproject.org blog.joinmastodon.org blog.elementary.io blog.gitbutler.com
""".split())
