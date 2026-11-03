# HN 独立博客索引（可访问性版）

从 Hacker News 20 年全库（6,236,741 帖子 / 43,051,020 评论，12.42 GB）挖掘。

## 与上一版的差别

| | 上一版（RSS 探测） | 本版（只验可访问） |
|---|---|---|
| 探测范围 | 前 600 名候选 | **全部 23,312 个候选** |
| 每域名请求数 | 最多 12 次（试 6–11 条 feed 路径） | **1 次**（抓首页） |
| 可访问 | — | **15,907（68%）** |
| 发现 feed | 232 | **7,537（32%）** |
| 最终入榜 | 167 | **5,910**（其中有 feed 2,728） |
| 耗时 | 约 5 分钟 | 约 21 分钟 |

关键做法：只抓首页一次，**同时**判定存活与解析 `<link rel=alternate>` 发现 feed。
省掉的是「盲试 /feed、/rss、/atom.xml…」那些注定失败的重复请求。

## 产物

- [`hn-blogs.opml`](hn-blogs.opml) —— **2728** 个可订阅源，分「精选 Top 300」和「完整」两组
- [`final.csv`](final.csv) —— 全部 **5910** 个可访问博客（含无 feed 的）
- [`no-feed.csv`](no-feed.csv) —— **3182** 个可访问但未自动发现 feed，需手动订阅
- 个人博客 **2724** / 团队博客 **4**（按 feed 计）

## 排序公式

```
score = min(p90, 600) × (0.4 + min(年数,12)/12) × (1 + min(log10(1+提及),3)/4) × (1 + min(篇数,40)/40×0.3)
```
- `p90` —— 该域名全部提交页面得分的 90 分位，比均值抗单篇爆款
- 持续性、讨论热度、产出量各为乘数，均有上限

## 前 60

| # | 域名 | 篇数 | p90 | 活跃年份 | 提及 | feed |
|---|---|---|---|---|---|---|
| 1 | [signal.org](https://signal.org) | 169 | 547 | 2016–2026 | 2,188 | ✅ |
| 2 | [ciechanow.ski](https://ciechanow.ski) | 90 | 733 | 2019–2026 | 696 | ✅ |
| 3 | [blog.samaltman.com](https://blog.samaltman.com) | 241 | 446 | 2013–2026 | 793 | ✅ |
| 4 | [krausefx.com](https://krausefx.com) | 35 | 630 | 2015–2026 | 44 | ✅ |
| 5 | [paulbutler.org](https://paulbutler.org) | 30 | 703 | 2009–2025 | 56 | ✅ |
| 6 | [blog.haschek.at](https://blog.haschek.at) | 61 | 432 | 2015–2026 | 110 | ✅ |
| 7 | [rosenzweig.io](https://rosenzweig.io) | 53 | 545 | 2018–2025 | 169 | ✅ |
| 8 | [chris-granger.com](https://chris-granger.com) | 45 | 402 | 2011–2024 | 192 | ✅ |
| 9 | [marctenbosch.com](https://marctenbosch.com) | 31 | 429 | 2010–2025 | 76 | ✅ |
| 10 | [antirez.com](https://antirez.com) | 296 | 328 | 2008–2026 | 647 | ✅ |
| 11 | [adriancourreges.com](https://adriancourreges.com) | 27 | 402 | 2015–2026 | 92 | ✅ |
| 12 | [jaycarlson.net](https://jaycarlson.net) | 21 | 535 | 2017–2026 | 56 | ✅ |
| 13 | [kalzumeus.com](https://kalzumeus.com) | 310 | 289 | 2008–2026 | 2,947 | ✅ |
| 14 | [jacquesmattheij.com](https://jacquesmattheij.com) | 458 | 287 | 2009–2026 | 966 | ✅ |
| 15 | [wozniak.ca](https://wozniak.ca) | 20 | 429 | 2014–2026 | 18 | ✅ |
| 16 | [awesomekling.github.io](https://awesomekling.github.io) | 26 | 570 | 2019–2023 | 106 | ✅ |
| 17 | [larslofgren.com](https://larslofgren.com) | 14 | 726 | 2012–2025 | 22 | ✅ |
| 18 | [andrewkelley.me](https://andrewkelley.me) | 80 | 269 | 2013–2026 | 273 | ✅ |
| 19 | [pushing-pixels.org](https://pushing-pixels.org) | 18 | 332 | 2008–2026 | 52 | ✅ |
| 20 | [stabyourself.net](https://stabyourself.net) | 10 | 420 | 2011–2025 | 64 | ✅ |
| 21 | [candyjapan.com](https://candyjapan.com) | 54 | 286 | 2012–2024 | 138 | ✅ |
| 22 | [blog.mecheye.net](https://blog.mecheye.net) | 38 | 284 | 2012–2024 | 64 | ✅ |
| 23 | [blog.benjojo.co.uk](https://blog.benjojo.co.uk) | 118 | 266 | 2015–2026 | 136 | ✅ |
| 24 | [karpathy.github.io](https://karpathy.github.io) | 89 | 241 | 2014–2026 | 475 | ✅ |
| 25 | [lexi-lambda.github.io](https://lexi-lambda.github.io) | 49 | 260 | 2015–2026 | 352 | ✅ |
| 26 | [blog.printf.net](https://blog.printf.net) | 12 | 393 | 2010–2024 | 82 | ✅ |
| 27 | [blog.pinboard.in](https://blog.pinboard.in) | 96 | 244 | 2011–2025 | 334 | ✅ |
| 28 | [sangaline.com](https://sangaline.com) | 13 | 521 | 2015–2025 | 40 | ✅ |
| 29 | [tinyprojects.dev](https://tinyprojects.dev) | 20 | 877 | 2020–2024 | 44 | ✅ |
| 30 | [fabiensanglard.net](https://fabiensanglard.net) | 378 | 225 | 2009–2026 | 905 | ✅ |
| 31 | [robert.ocallahan.org](https://robert.ocallahan.org) | 152 | 245 | 2011–2025 | 222 | ✅ |
| 32 | [play0ad.com](https://play0ad.com) | 33 | 262 | 2013–2026 | 144 | ✅ |
| 33 | [bzarg.com](https://bzarg.com) | 21 | 390 | 2015–2024 | 64 | ✅ |
| 34 | [aphyr.com](https://aphyr.com) | 206 | 220 | 2011–2026 | 1,247 | ✅ |
| 35 | [jsomers.net](https://jsomers.net) | 146 | 242 | 2008–2026 | 189 | ✅ |
| 36 | [framablog.org](https://framablog.org) | 25 | 382 | 2018–2025 | 48 | ✅ |
| 37 | [sam.zeloof.xyz](https://sam.zeloof.xyz) | 15 | 502 | 2018–2025 | 98 | ✅ |
| 38 | [tonsky.me](https://tonsky.me) | 202 | 229 | 2014–2026 | 349 | ✅ |
| 39 | [neustadt.fr](https://neustadt.fr) | 13 | 448 | 2015–2026 | 14 | ✅ |
| 40 | [marcan.st](https://marcan.st) | 16 | 352 | 2016–2025 | 96 | ✅ |
| 41 | [bugs.xdavidhu.me](https://bugs.xdavidhu.me) | 14 | 1065 | 2020–2026 | 8 | ✅ |
| 42 | [troyhunt.com](https://troyhunt.com) | 616 | 210 | 2010–2026 | 928 | ✅ |
| 43 | [bert.org](https://bert.org) | 24 | 401 | 2018–2026 | 18 | ✅ |
| 44 | [overreacted.io](https://overreacted.io) | 114 | 267 | 2018–2026 | 472 | ✅ |
| 45 | [tomrenner.com](https://tomrenner.com) | 8 | 632 | 2021–2026 | 12 | ✅ |
| 46 | [casparwre.de](https://casparwre.de) | 12 | 719 | 2020–2024 | 8 | ✅ |
| 47 | [mchap.io](https://mchap.io) | 10 | 541 | 2018–2025 | 36 | ✅ |
| 48 | [openrss.org](https://openrss.org) | 9 | 639 | 2022–2026 | 38 | ✅ |
| 49 | [tom.preston-werner.com](https://tom.preston-werner.com) | 71 | 223 | 2008–2025 | 278 | ✅ |
| 50 | [mzucker.github.io](https://mzucker.github.io) | 21 | 395 | 2016–2025 | 22 | ✅ |
| 51 | [nixos.org](https://nixos.org) | 72 | 204 | 2011–2026 | 1,864 | ✅ |
| 52 | [dcurt.is](https://dcurt.is) | 148 | 226 | 2011–2025 | 212 | ✅ |
| 53 | [matt.sh](https://matt.sh) | 41 | 241 | 2013–2024 | 82 | ✅ |
| 54 | [neilwithdata.com](https://neilwithdata.com) | 10 | 611 | 2020–2026 | 28 | ✅ |
| 55 | [foundersatwork.posthaven.com](https://foundersatwork.posthaven.com) | 38 | 291 | 2014–2025 | 38 | ✅ |
| 56 | [tyler.io](https://tyler.io) | 42 | 337 | 2014–2026 | 28 | ✅ |
| 57 | [peabee.substack.com](https://peabee.substack.com) | 14 | 645 | 2022–2025 | 16 | ✅ |
| 58 | [somethingsimilar.com](https://somethingsimilar.com) | 24 | 307 | 2012–2025 | 18 | ✅ |
| 59 | [os.phil-opp.com](https://os.phil-opp.com) | 50 | 232 | 2015–2025 | 212 | ✅ |
| 60 | [incolumitas.com](https://incolumitas.com) | 18 | 337 | 2016–2026 | 44 | ✅ |

## 被反复提起的文章（每站≤3）

| 年份跨度 | 提及 | 站点 | 文章 |
|---|---|---|---|
| 20 年 | 734 | paulgraham.com | [PG: What You Can't Say (2004)](http://paulgraham.com/say.html) |
| 20 年 | 929 | paulgraham.com | [Lisp as a secret weapon](http://www.paulgraham.com/avg.html) |
| 20 年 | 1,772 | paulgraham.com | [The Submarine (2005)](http://www.paulgraham.com/submarine.html) |
| 18 年 | 174 | idlewords.com | [Dabblers and Blowhards (2005)](http://www.idlewords.com/2005/04/dabblers_and_blowhards.htm) |
| 17 年 | 300 | stallman.org | [Richard Stallman: How I do my Computing](http://stallman.org/stallman-computing.html) |
| 17 年 | 276 | kalzumeus.com | [Falsehoods Programmers Believe About Names](http://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/) |
| 16 年 | 148 | kalzumeus.com | [Don't Call Yourself A Programmer, And Other Career Advice (2011)](http://www.kalzumeus.com/2011/10/28/dont-call-yourself-a-programmer/) |
| 15 年 | 299 | kalzumeus.com | [Salary Negotiation: Make More Money, Be More Valued](http://www.kalzumeus.com/2012/01/23/salary-negotiation/) |
| 16 年 | 96 | idlewords.com | [Scott and Scurvy: How the Royal Navy forgot its cure (2010)](http://idlewords.com/2010/03/scott_and_scurvy.htm) |
| 15 年 | 70 | antirez.com | [Tcl the misunderstood (2006)](http://antirez.com/articoli/tclmisunderstood.html) |
| 15 年 | 76 | stallman.org | [Stallman on Hacking](http://stallman.org/articles/on-hacking.html) |
| 15 年 | 43 | byorgey.wordpress.com | [Abstraction, intuition, and the “monad tutorial fallacy” (2009)](https://byorgey.wordpress.com/2009/01/12/abstraction-intuition-and-the-monad-tutorial-fallacy/) |
| 12 年 | 110 | sockpuppet.org | [The hiring post](https://sockpuppet.org/blog/2015/03/06/the-hiring-post/) |
| 13 年 | 67 | stallman.org | [Reasons Not to Buy from Amazon](https://stallman.org/amazon.html) |
| 13 年 | 48 | idlewords.com | [A Rocket to Nowhere (2005)](https://idlewords.com/2005/08/a_rocket_to_nowhere.htm#8) |
| 12 年 | 52 | blog.chriszacharias.com | [Page Weight Matters (2012)](http://blog.chriszacharias.com/page-weight-matters) |
| 13 年 | 19 | betterexplained.com | [A Visual, Intuitive Guide to Imaginary Numbers](http://betterexplained.com/articles/a-visual-intuitive-guide-to-imaginary-numbers/) |
| 11 年 | 201 | karpathy.github.io | [The Unreasonable Effectiveness of Recurrent Neural Networks](http://karpathy.github.io/2015/05/21/rnn-effectiveness/) |
| 11 年 | 98 | sandimetz.com | [The Wrong Abstraction](http://www.sandimetz.com/blog/2016/1/20/the-wrong-abstraction) |
| 12 年 | 86 | akkartik.name | [I'm working on ways to better convey the global structure of programs (2013)](http://akkartik.name/about) |
| 12 年 | 48 | bunniestudios.com | [Tech Trend: Shanzhai (2009)](https://www.bunniestudios.com/blog/?p=284) |
| 11 年 | 120 | sockpuppet.org | [Against DNSSEC](https://sockpuppet.org/blog/2015/01/15/against-dnssec/) |
| 12 年 | 36 | blog.rongarret.info | [Parallel universes and the arrow of time (2014)](http://blog.rongarret.info/2014/10/parallel-universes-and-arrow-of-time.html) |
| 10 年 | 186 | signal.org | [Technology preview: Private contact discovery for Signal](https://signal.org/blog/private-contact-discovery/) |
| 10 年 | 166 | blog.burntsushi.net | [Ripgrep is faster (2016)](https://blog.burntsushi.net/ripgrep/) |
| 11 年 | 23 | randomascii.wordpress.com | [There Are Only Four Billion Floats – So Test Them All](http://randomascii.wordpress.com/2014/01/27/theres-only-four-billion-floatsso-test-them-all/) |
| 11 年 | 112 | aphyr.com | [https://aphyr.com/tags/jepsen](https://aphyr.com/tags/jepsen) |
| 11 年 | 102 | stavros.io | [Attic: The Holy Grail of Backups](http://www.stavros.io/posts/holy-grail-backups/) |
| 10 年 | 88 | aphyr.com | [Hexing the technical interview](https://aphyr.com/posts/341-hexing-the-technical-interview) |
| 11 年 | 22 | trixter.oldskool.org | [8088 MPH: We Break All Your Emulators](http://trixter.oldskool.org/2015/04/07/8088-mph-we-break-all-your-emulators/) |
| 10 年 | 64 | blog.pinboard.in | [Don't Be A Free User](https://blog.pinboard.in/2011/12/don_t_be_a_free_user/) |
| 10 年 | 72 | bunniestudios.com | [On Hacking MicroSD cards (2013)](http://www.bunniestudios.com/blog/?p=3554) |
| 10 年 | 218 | signal.org | [Reflections: The Ecosystem Is Moving](https://signal.org/blog/the-ecosystem-is-moving/) |
| 10 年 | 42 | graydon2.dreamwidth.org | [Always Bet on Text (2014)](https://graydon2.dreamwidth.org/193447.html) |
| 11 年 | 35 | byorgey.wordpress.com | [https://byorgey.wordpress.com/2009/01/12/abstraction-intuiti...](https://byorgey.wordpress.com/2009/01/12/abstraction-intuiti...) |
| 10 年 | 27 | bjk5.com | [Breaking down Amazon’s mega dropdown (2013)](http://bjk5.com/post/44698559168/breaking-down-amazons-mega-dropdown) |
| 11 年 | 16 | betterexplained.com | [Understanding Quake's Fast Inverse Square Root](https://betterexplained.com/articles/understanding-quakes-fast-inverse-square-root/) |
| 10 年 | 24 | bzarg.com | [How a Kalman filter works, in pictures](https://www.bzarg.com/p/how-a-kalman-filter-works-in-pictures/) |
| 9 年 | 112 | aphyr.com | [Typing the technical interview](https://aphyr.com/posts/342-typing-the-technical-interview) |
| 10 年 | 28 | betterexplained.com | [An Interactive Guide to the Fourier Transform](http://betterexplained.com/articles/an-interactive-guide-to-the-fourier-transform/) |

## 已知局限

- **「可访问」≠「还活着」**：死掉的博客首页照样返回 200。本版只证明站点还在，不证明还在更新。要判断更新，必须抓 feed 看最近条目时间。
- **精度下降**：探测范围扩大 39 倍后，产品页/项目站混了进来（如 `iterm2.com`、`pandoc.org`、`starlink.com`），URL 形态无法自动区分——`paulgraham.com` 全是文章却零特征，`iterm2.com` 反而有特征。彻底解决需要 LLM 看首页内容。
- **评论侧仍只抓带链接的提及**（5.16M/43.05M 条评论含 URL），纯文字提及未覆盖。
- **未过滤 deleted/dead 字段**。