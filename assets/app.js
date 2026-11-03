'use strict';

/* --------------------------------------------------------------------------
   Hacker Blogs · a card catalog
   Colour is not a random hash: each subject owns one ink, shared by the
   sidebar dot, the card band, and the drawer mark.
   -------------------------------------------------------------------------- */

const SUBJECTS = {
  '系统与内核':   { h: 255, l: 0.50, c: 0.085 },
  '数据与 AI':    { h: 300, l: 0.52, c: 0.095 },
  '语言与编译器': { h: 28,  l: 0.53, c: 0.100 },
  '硬件与底层':   { h: 150, l: 0.50, c: 0.075 },
  'Web 与前端':   { h: 205, l: 0.53, c: 0.085 },
  '安全与隐私':   { h: 15,  l: 0.52, c: 0.120 },
  '职业与创业':   { h: 70,  l: 0.55, c: 0.090 },
  '设计':         { h: 340, l: 0.54, c: 0.100 },
  '科学与思想':   { h: 120, l: 0.48, c: 0.060 },
  '数学':         { h: 280, l: 0.48, c: 0.090 },
  '其他':         { h: 70,  l: 0.53, c: 0.012 },
};

const SUBJECT_LABELS = {
  en: {
    '系统与内核': 'Systems & kernels',
    '数据与 AI': 'Data & AI',
    '语言与编译器': 'Languages & compilers',
    '硬件与底层': 'Hardware & low level',
    'Web 与前端': 'Web & frontend',
    '安全与隐私': 'Security & privacy',
    '职业与创业': 'Career & startups',
    '设计': 'Design',
    '科学与思想': 'Science & ideas',
    '数学': 'Math',
    '其他': 'Other',
  },
  zh: {},
};

const SUBJECT_SHORT = {
  en: {
    '系统与内核': 'Systems',
    '数据与 AI': 'Data',
    '语言与编译器': 'Languages',
    '硬件与底层': 'Hardware',
    'Web 与前端': 'Web',
    '安全与隐私': 'Security',
    '职业与创业': 'Career',
    '设计': 'Design',
    '科学与思想': 'Science',
    '数学': 'Math',
    '其他': 'Other',
  },
  zh: {},
};

const I18N = {
  en: {
    title: 'Hacker Blogs · an independent blog catalog from 20 years of HN',
    desc: 'A catalog of independent blogs and the posts HN keeps citing, mined from twenty years and 49 million records.',
    skip: 'Skip to content',
    searchLabel: 'Search',
    searchPh: 'Search domain, title, topic',
    langLabel: 'Language',

    navAll: 'All blogs',
    navFeed: 'Subscribable',
    navPosts: 'Most-cited posts',

    sideTopics: 'Topics',
    sideEras: 'First seen',
    figBlogs: 'sites',
    figPosts: 'posts',
    figRecords: 'raw records',
    dlTitle: 'Subscribe by RSS',
    dlAll: 'Download all 2,241 sites',
    dlTop: 'Download top 300 sites',
    allTopics: 'All',


    allTitle: 'All blogs',
    allFeedTitle: 'Subscribable blogs',
    results: 'results',
    resultOne: 'result',
    keyword: 'keyword',
    firstSeen: 'first seen',

    chipType: 'Type',
    chipPersonal: 'Blogs',
    chipAllSites: 'All sites',
    chipFeed: 'Feed',
    chipAll: 'All',
    chipHasFeed: 'Has RSS',
    chipFirstSeen: 'First seen',
    chipAny: 'Any',
    chipPre2010: 'Before 2010',
    chip2010s: '2010s',
    chip2020s: '2020s',
    sortLabel: 'Sort',
    sortScore: 'Composite',
    sortP90: 'Post quality p90',
    sortYears: 'Active years',
    sortMentions: 'Mentions',
    sortAz: 'Domain A-Z',
    more: 'Load more',
    moreLeft: 'left',

    postsTitle: 'Most-cited posts',
    postsLead: 'Ranked by how many distinct years a URL was cited. Four per site at most. Fifteen years of repeats is what makes a classic.',
    postsSpan: 'Span',
    span5: 'Five years',
    span10: 'Ten years',
    span15: 'Fifteen years',
    prevPage: 'Previous',
    nextPage: 'Next',
    firstPage: 'First',
    lastPage: 'Last',
    pageFmt: 'Page {p} of {n}',
    postsCount: 'posts',
    postsTopic: 'Topic',
    postsAll: 'All',
    cited: 'cited',
    peak: 'peak',

    empty: 'No matches',
    stamp: 'No feed',
    yrs: 'yrs',

    dSubmitted: 'Submitted',
    dP90: 'p90',
    dYears: 'Years',
    dMentions: 'Mentions',
    dActive: 'Active years',
    dPosts: 'Most-cited posts',
    dNoPosts: 'No multi-year posts yet',
    dRelated: 'More in this topic',
    dOpen: 'Open site',
    dRss: 'RSS',
    dCopy: 'Copy domain',
    dCopied: 'Copied',
    close: 'Close',
    loadError: 'Could not load data: ',
  },
  zh: {
    title: 'Hacker Blogs · 二十年 HN 的独立博客目录',
    desc: '从 Hacker News 二十年、四千九百万条数据里整理的独立博客目录，以及被反复引用的文章。',
    skip: '跳到主内容',
    searchLabel: '搜索',
    searchPh: '搜域名、标题、主题',
    langLabel: '语言',

    navAll: '全部博客',
    navFeed: '可订阅',
    navPosts: '反复被推荐的文章',

    sideTopics: '主题',
    sideEras: '首次出现',
    figBlogs: '个站点',
    figPosts: '篇文章',
    figRecords: '条原始记录',
    dlTitle: 'RSS 订阅',
    dlAll: '下载全部 2,241 个站点',
    dlTop: '下载精选 300 个站点',
    allTopics: '全部',


    allTitle: '全部博客',
    allFeedTitle: '可订阅的博客',
    results: '个结果',
    resultOne: '个结果',
    keyword: '关键词',
    firstSeen: '首发',

    chipType: '类型',
    chipPersonal: '博客',
    chipAllSites: '全部站点',
    chipFeed: '订阅',
    chipAll: '全部',
    chipHasFeed: '有 RSS',
    chipFirstSeen: '首次出现',
    chipAny: '不限',
    chipPre2010: '2010 前',
    chip2010s: '2010 年代',
    chip2020s: '2020 年代',
    sortLabel: '排序',
    sortScore: '综合分',
    sortP90: '单篇质量 p90',
    sortYears: '活跃年数',
    sortMentions: '评论提及',
    sortAz: '域名 A-Z',
    more: '加载更多',
    moreLeft: '还有',

    postsTitle: '反复被推荐的文章',
    postsLead: '按被引用的不同年份数排序。每站最多四篇。跨十五年还在被链接的，才算经典。',
    postsSpan: '跨度',
    span5: '五年以上',
    span10: '十年以上',
    span15: '十五年以上',
    prevPage: '上一页',
    nextPage: '下一页',
    firstPage: '首页',
    lastPage: '末页',
    pageFmt: '第 {p} 页 / 共 {n} 页',
    postsCount: '篇',
    postsTopic: '主题',
    postsAll: '全部',
    cited: '提及',
    peak: '最高',

    empty: '没有匹配的结果',
    stamp: '无 RSS',
    yrs: '年',

    dSubmitted: '提交',
    dP90: 'p90',
    dYears: '年',
    dMentions: '提及',
    dActive: '活跃年份',
    dPosts: '被反复推荐的文章',
    dNoPosts: '暂无跨年重复推荐的文章',
    dRelated: '同主题的其它博客',
    dOpen: '打开站点',
    dRss: 'RSS',
    dCopy: '复制域名',
    dCopied: '已复制',
    close: '关闭',
    loadError: '数据加载失败：',
  },
};

let lang = localStorage.getItem('hb-lang') || 'en';
if (!I18N[lang]) lang = 'en';

const t = (k) => (I18N[lang] && I18N[lang][k]) || I18N.en[k] || k;
const nf = (n) => Number(n).toLocaleString(lang === 'zh' ? 'zh-CN' : 'en-US');
const subjLabel = (s) => (SUBJECT_LABELS[lang] && SUBJECT_LABELS[lang][s]) || s;
const subjShort = (s) => (SUBJECT_SHORT[lang] && SUBJECT_SHORT[lang][s]) || subjLabel(s);
const locale = () => (lang === 'zh' ? 'zh-CN' : 'en-US');

function band(subject) {
  const s = SUBJECTS[subject] || SUBJECTS['其他'];
  return `oklch(${s.l} ${s.c} ${s.h})`;
}
function tint(subject) {
  const s = SUBJECTS[subject] || SUBJECTS['其他'];
  return `oklch(0.972 ${Math.min(s.c, 0.010)} ${s.h})`;
}

const state = {
  blogs: [], posts: [], postByDomain: new Map(),
  view: 'posts', q: '', topic: null, eraRange: null,
  feedOnly: false, sort: 'score', limit: 120, postMinYears: 0, postPage: 1,
  postTopic: null,
  showCompany: false,
};

const $ = (s) => document.querySelector(s);
const $$ = (s) => [...document.querySelectorAll(s)];

const esc = (s) => String(s).replace(/[&<>"]/g,
  (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

function hash(str) {
  let h = 2166136261;
  for (let i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); }
  return h >>> 0;
}
function mulberry32(a) {
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function monogram(domain) {
  const label = domain.replace(/^www\./, '').split('.')[0].replace(/[^a-z0-9]/gi, '');
  return (label.slice(0, 2) || domain[0] || '?').toUpperCase();
}

/* ---------- data ---------- */
async function load() {
  const [b, p] = await Promise.all([
    fetch('data/blogs.json').then((r) => r.json()),
    fetch('data/posts.json').then((r) => r.json()),
  ]);
  state.blogs = b;
  state.posts = p;
  for (const post of p) {
    if (!state.postByDomain.has(post.d)) state.postByDomain.set(post.d, []);
    state.postByDomain.get(post.d).push(post);
  }
  figures();
  buildSidebar();
  render();
}

function figures() {
  $('#s-blogs').textContent = nf(state.blogs.length);
  $('#s-posts').textContent = nf(state.posts.length);
}

/* ---------- sidebar ---------- */
function typePool() {
  return state.showCompany ? state.blogs : state.blogs.filter((b) => b.kind !== 'company');
}

function buildSidebar() {
  const pool = typePool();
  const counts = new Map();
  for (const b of pool) for (const tp of b.topics) counts.set(tp, (counts.get(tp) || 0) + 1);
  const topics = [...counts.entries()].sort((a, b) => b[1] - a[1]);

  $('#topics').innerHTML =
    `<a data-topic="" class="${state.topic ? '' : 'is-on'}">${esc(t('allTopics'))}<span class="n">${nf(pool.length)}</span></a>`
    + topics.map(([tp, n]) =>
      `<a data-topic="${esc(tp)}" class="${state.topic === tp ? 'is-on' : ''}">
        <i class="dot" style="--dot:${band(tp)}"></i><span class="tlabel">${esc(subjLabel(tp))}</span>
        <span class="n">${nf(n)}</span></a>`).join('');

  const eras = [['2007-2012', 2012], ['2013-2017', 2017], ['2018-2022', 2022], ['2023-2026', 2026]];
  $('#eras').innerHTML = eras.map(([label, max], i) => {
    const min = i === 0 ? 2006 : eras[i - 1][1] + 1;
    const n = pool.filter((b) => b.first >= min && b.first <= max).length;
    const on = state.eraRange && state.eraRange[0] === min ? 'is-on' : '';
    return `<a data-era="${min}-${max}" class="${on}">${label}<span class="n">${nf(n)}</span></a>`;
  }).join('');
}

function syncNav() {
  $$('#views .nav-item').forEach((x) =>
    x.classList.toggle('is-active', x.dataset.view === state.view));
}

/* ---------- filter ---------- */
function filtered() {
  const q = state.q.trim().toLowerCase();
  let list = state.blogs;
  if (state.topic) list = list.filter((b) => b.topics.includes(state.topic));
  if (state.eraRange) {
    const [min, max] = state.eraRange;
    list = list.filter((b) => b.first >= min && b.first <= max);
  }
  if (state.feedOnly) list = list.filter((b) => b.has_feed);
  if (!state.showCompany) list = list.filter((b) => b.kind !== 'company');
  if (q) {
    list = list.filter((b) => b.domain.includes(q)
      || (b.title || '').toLowerCase().includes(q)
      || b.topics.some((tp) => tp.toLowerCase().includes(q)
        || subjLabel(tp).toLowerCase().includes(q)));
  }
  const s = state.sort;
  return [...list].sort((a, b) =>
    s === 'az' ? a.domain.localeCompare(b.domain) : (b[s] || 0) - (a[s] || 0));
}

/* ---------- card ---------- */
function cardHTML(b, i) {
  const subj = b.topics[0] || '其他';
  const stamp = b.has_feed ? '' : `<span class="stamp">${esc(t('stamp'))}</span>`;
  const ticks = [];
  for (let k = 0; k < 21; k++) {
    ticks.push(`<i class="${(b.ya >> k) & 1 ? 'on' : ''}"></i>`);
  }
  return `<button class="card" data-d="${esc(b.domain)}" style="--i:${i}"
      aria-label="${esc(b.domain)}, ${b.posts} posts, ${b.first} to ${b.last}"
      title="${esc(b.intro || '')}">
    <span class="card-art" style="--tint:${tint(subj)};--band:${band(subj)}">
      ${stamp}
      <span class="card-year">${b.first}</span>
      <span class="card-spark" aria-hidden="true">${ticks.join('')}</span>
      <span class="card-band"><span>${esc(subjShort(subj))}</span><em>${b.posts}</em></span>
    </span>
    <span class="card-meta">
      <span class="card-name">${esc(b.domain)}</span>
      <span class="card-sub">${b.years} ${esc(t('yrs'))} · p90 ${Math.round(b.p90)}</span>
    </span>
  </button>`;
}

/* ---------- views ---------- */
function render() {
  const isPosts = state.view === 'posts';
  $('#all-view').hidden = isPosts;
  $('#posts-view').hidden = !isPosts;
  if (isPosts) return renderPosts();
  renderAll();
}

function renderAll() {
  const list = filtered();
  const shown = list.slice(0, state.limit);
  $('#all-title').textContent = state.topic
    ? subjLabel(state.topic)
    : (state.feedOnly ? t('allFeedTitle') : t('allTitle'));

  let sub = `<b>${nf(list.length)}</b> ${esc(t('results'))}`;
  if (state.q) sub += ` · ${esc(t('keyword'))} “${esc(state.q)}”`;
  if (state.eraRange) sub += ` · ${esc(t('firstSeen'))} ${state.eraRange[0]}–${state.eraRange[1]}`;
  $('#all-sub').innerHTML = sub;

  $('#all-grid').innerHTML = shown.length
    ? shown.map(cardHTML).join('')
    : `<div class="empty">${esc(t('empty'))}</div>`;
  $('#more').hidden = list.length <= shown.length;
  $('#more').textContent = lang === 'zh'
    ? `${t('more')}（${t('moreLeft')} ${nf(list.length - shown.length)} 个）`
    : `${t('more')} (${nf(list.length - shown.length)} ${t('moreLeft')})`;
}

function postPool() {
  return state.posts.filter((p) => p.y >= state.postMinYears
    && (!state.postTopic || p.tp === state.postTopic));
}

function buildPostTopics() {
  const counts = new Map();
  for (const p of state.posts) counts.set(p.tp, (counts.get(p.tp) || 0) + 1);
  const items = [...counts.entries()].sort((a, b) => b[1] - a[1]);
  $('#post-topics').innerHTML =
    `<span class="chip-label">${esc(t('postsTopic'))}</span>
     <button class="chip ${state.postTopic ? '' : 'is-on'}" data-tp="">${esc(t('postsAll'))}</button>`
    + items.map(([tp, n]) =>
      `<button class="chip ${state.postTopic === tp ? 'is-on' : ''}" data-tp="${esc(tp)}"
         style="--dot:${band(tp)}">${esc(subjLabel(tp))}
         <span class="chip-n">${nf(n)}</span></button>`).join('');
}

function renderPosts() {
  buildPostTopics();
  const all = postPool();
  const per = 100;
  const pages = Math.max(1, Math.ceil(all.length / per));
  state.postPage = Math.min(Math.max(1, state.postPage), pages);
  const start = (state.postPage - 1) * per;
  const list = all.slice(start, start + per);

  const total = state.posts.filter((p) => p.y >= state.postMinYears).length;
  $('#posts-sub').innerHTML = state.postTopic
    ? `<b>${nf(all.length)}</b> ${esc(t('postsCount'))} · ${esc(subjLabel(state.postTopic))} · ${nf(total)} ${esc(t('postsCount'))} total`
    : `<b>${nf(all.length)}</b> ${esc(t('postsCount'))}`;

  $('#post-list').innerHTML = list.length ? list.map((p, i) => `
    <li class="post-row">
      <div class="post-rank">${start + i + 1}</div>
      <div class="post-years">${p.y}<span>${esc(t('yrs'))}</span></div>
      <div>
        <a class="post-title" href="${esc(p.u)}" target="_blank" rel="noopener">${esc(p.t)}</a>
        <div class="post-sub"><b>${esc(p.d)}</b> · ${esc(t('cited'))} ${nf(p.m)} · ${esc(t('peak'))} ${p.s}</div>
      </div>
      <div class="post-score">${p.sc}</div>
    </li>`).join('') : `<div class="empty">${esc(t('empty'))}</div>`;

  const btn = (act, label, dis) =>
    `<button class="pg" data-pg="${act}" ${dis ? 'disabled' : ''} aria-label="${esc(label)}">${esc(label)}</button>`;
  $('#post-pager').innerHTML = pages > 1 ? `
    ${btn('first', t('firstPage'), state.postPage === 1)}
    ${btn('prev', t('prevPage'), state.postPage === 1)}
    <span class="pg-info">${esc(t('pageFmt').replace('{p}', state.postPage).replace('{n}', pages))}</span>
    ${btn('next', t('nextPage'), state.postPage === pages)}
    ${btn('last', t('lastPage'), state.postPage === pages)}` : '';
  $('#post-pager').hidden = pages <= 1;
}

/* ---------- drawer ---------- */
let lastFocus = null;

function openDrawer(domain) {
  const b = state.blogs.find((x) => x.domain === domain);
  if (!b) return;
  const subj = b.topics[0] || '其他';
  const posts = (state.postByDomain.get(domain) || []).slice(0, 6);
  const mono = monogram(domain);
  const siblings = state.blogs
    .filter((x) => x.domain !== domain && (x.topics[0] || '其他') === subj)
    .sort((a, b) => b.score - a.score)
    .slice(0, 6);

  $('#drawer-body').innerHTML = `
    <div class="d-mark">
      <div class="d-badge" style="--tint:${tint(subj)}">${esc(mono)}</div>
      <div style="min-width:0">
        <div class="d-name">${esc(b.domain)}</div>
        <button class="d-subject" data-subj="${esc(subj)}" style="--band:${band(subj)}">
          <i></i>${esc(subjLabel(subj))}<span>·</span>${b.has_feed ? 'RSS' : esc(t('stamp'))}</button>
        <p class="d-intro">${esc(b.intro || '')}</p>
      </div>
    </div>
    <hr class="d-rule">
    <div class="d-figs">
      <div class="d-fig"><b>${b.posts}</b><span>${esc(t('dSubmitted'))}</span></div>
      <div class="d-fig"><b>${Math.round(b.p90)}</b><span>${esc(t('dP90'))}</span></div>
      <div class="d-fig"><b>${b.years}</b><span>${esc(t('dYears'))}</span></div>
      <div class="d-fig"><b>${nf(b.mentions)}</b><span>${esc(t('dMentions'))}</span></div>
    </div>
    <hr class="d-rule">
    <div class="d-sec-title">${esc(t('dActive'))}</div>
    <div class="d-spark" style="--band:${band(subj)}" aria-hidden="true">${
      Array.from({ length: 21 }, (_, k) => `<i class="${(b.ya >> k) & 1 ? 'on' : ''}"></i>`).join('')
    }</div>
    <div class="d-axis"><span>2006</span><span>2026</span></div>
    <hr class="d-rule">
    ${posts.length
      ? `<div class="d-sec-title">${esc(t('dPosts'))}</div>` + posts.map((p) => `
        <div class="d-post"><span class="yrs">${p.y}y</span>
          <a href="${esc(p.u)}" target="_blank" rel="noopener">${esc(p.t)}</a></div>`).join('')
      : `<div class="d-sec-title">${esc(t('dNoPosts'))}</div>`}
    <hr class="d-rule">
    <div class="d-sec-title">${esc(t('dRelated'))}</div>
    <div class="d-sibs">${siblings.map((x) =>
      `<button class="d-sib" data-open="${esc(x.domain)}">${esc(x.domain)}</button>`).join('')}</div>
    <div class="d-actions">
      <a class="d-btn solid" href="https://${esc(b.domain)}" target="_blank" rel="noopener">${esc(t('dOpen'))}</a>
      ${b.feed ? `<a class="d-btn" href="${esc(b.feed)}" target="_blank" rel="noopener">${esc(t('dRss'))}</a>` : ''}
      <button class="d-btn" data-copy="${esc(b.domain)}">${esc(t('dCopy'))}</button>
    </div>`;

  lastFocus = document.activeElement;
  const drawer = $('#drawer');
  drawer.hidden = false;
  $('#scrim').hidden = false;
  drawer.classList.add('is-entering');
  requestAnimationFrame(() => drawer.classList.remove('is-entering'));
  $('.drawer-x').focus({ preventScroll: true });
  document.body.style.overflow = 'hidden';
}

function closeDrawer() {
  const drawer = $('#drawer');
  if (drawer.hidden) return;
  drawer.hidden = true;
  $('#scrim').hidden = true;
  document.body.style.overflow = '';
  if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
}

/* ---------- language ---------- */
function applyLang() {
  const isZh = lang === 'zh';
  document.documentElement.lang = isZh ? 'zh-CN' : 'en';
  document.title = t('title');
  const meta = document.querySelector('meta[name="description"]');
  if (meta) meta.setAttribute('content', t('desc'));

  $$('[data-i18n]').forEach((el) => { el.textContent = t(el.dataset.i18n); });
  $$('[data-i18n-ph]').forEach((el) => { el.setAttribute('placeholder', t(el.dataset.i18nPh)); });
  $$('[data-i18n-aria]').forEach((el) => { el.setAttribute('aria-label', t(el.dataset.i18nAria)); });

  $$('.lang button').forEach((b) => {
    const on = b.dataset.lang === lang;
    b.classList.toggle('is-on', on);
    b.setAttribute('aria-pressed', String(on));
  });

  closeDrawer();
  figures();
  buildSidebar();
  render();
}

function setLang(next) {
  if (!I18N[next] || next === lang) return;
  lang = next;
  localStorage.setItem('hb-lang', lang);
  applyLang();
}

/* ---------- wiring ---------- */
function wire() {
  $$('.lang button').forEach((b) =>
    b.addEventListener('click', () => setLang(b.dataset.lang)));

  $$('#views .nav-item').forEach((a) => a.addEventListener('click', (e) => {
    e.preventDefault();
    state.view = a.dataset.view;
    if (state.view === 'feed') {
      state.feedOnly = true; state.topic = null; state.eraRange = null;
      $$('#topics a').forEach((x) => x.classList.toggle('is-on', !x.dataset.topic));
      $$('#eras a').forEach((x) => x.classList.remove('is-on'));
    } else if (state.view === 'all') {
      state.feedOnly = false;
    }
    state.limit = 120;
    syncNav();
    render();
  }));

  $('#topics').addEventListener('click', (e) => {
    const a = e.target.closest('a');
    if (!a) return;
    e.preventDefault();
    state.topic = a.dataset.topic || null;
    $$('#topics a').forEach((x) => x.classList.toggle('is-on', x === a));
    if (state.view !== 'all') { state.view = 'all'; syncNav(); }
    state.limit = 120;
    render();
  });

  $('#eras').addEventListener('click', (e) => {
    const a = e.target.closest('a');
    if (!a) return;
    e.preventDefault();
    const was = a.classList.contains('is-on');
    const [min, max] = a.dataset.era.split('-').map(Number);
    $$('#eras a').forEach((x) => x.classList.toggle('is-on', x === a && !was));
    state.eraRange = was ? null : [min, max];
    if (state.view !== 'all') { state.view = 'all'; syncNav(); }
    state.limit = 120;
    render();
  });

  $('#all-chips').addEventListener('click', (e) => {
    const chip = e.target.closest('.chip');
    if (!chip) return;
    if (chip.dataset.f) {
      [...chip.parentElement.children].forEach((c) => c.classList.toggle('is-on', c === chip));
      state.feedOnly = chip.dataset.f === 'feed';
      state.limit = 120;
      render();
    }
    if (chip.dataset.c) {
      [...chip.parentElement.children].forEach((c) => c.classList.toggle('is-on', c === chip));
      state.showCompany = chip.dataset.c === 'all';
      state.limit = 120;
      buildSidebar();
      render();
    }
    if (chip.dataset.e) {
      [...chip.parentElement.children].forEach((c) => c.classList.toggle('is-on', c === chip));
      const v = Number(chip.dataset.e);
      state.eraRange = v === 0 ? null : (v === 2010 ? [2006, 2009] : (v === 2020 ? [2010, 2019] : [2020, 2026]));
      state.limit = 120;
      render();
    }
  });

  $('#post-pager').addEventListener('click', (e) => {
    const b = e.target.closest('[data-pg]');
    if (!b || b.disabled) return;
    const total = Math.max(1, Math.ceil(
      postPool().length / 100));
    const map = { first: 1, prev: state.postPage - 1, next: state.postPage + 1, last: total };
    state.postPage = Math.min(Math.max(1, map[b.dataset.pg]), total);
    renderPosts();
    document.getElementById('posts-view').scrollIntoView({ block: 'start' });
  });

  $('#post-chips').addEventListener('click', (e) => {
    const chip = e.target.closest('.chip');
    if (!chip) return;
    if (chip.dataset.tp !== undefined && chip.hasAttribute('data-tp')) {
      state.postTopic = chip.dataset.tp || null;
      state.postPage = 1;
      renderPosts();
      return;
    }
    [...chip.parentElement.children].forEach((c) => c.classList.toggle('is-on', c === chip));
    state.postMinYears = Number(chip.dataset.p);
    state.postPage = 1;
    renderPosts();
  });

  $('#sort').addEventListener('change', (e) => {
    state.sort = e.target.value;
    state.limit = 120;
    renderAll();
  });

  $('#more').addEventListener('click', () => {
    state.limit += 120;
    renderAll();
  });

  $('#q').addEventListener('input', (e) => {
    state.q = e.target.value;
    state.limit = 120;
    if (state.view === 'posts') { state.view = 'all'; syncNav(); }
    render();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === '/' && document.activeElement !== $('#q')) {
      e.preventDefault();
      $('#q').focus();
    }
    if (e.key === 'Escape') closeDrawer();
  });

  document.addEventListener('click', (e) => {
    const open = e.target.closest('[data-open]');
    if (open) return openDrawer(open.dataset.open);
    const card = e.target.closest('.card');
    if (card) return openDrawer(card.dataset.d);
    if (e.target.closest('.drawer-x') || e.target.id === 'scrim') return closeDrawer();
    const subj = e.target.closest('[data-subj]');
    if (subj) {
      state.topic = subj.dataset.subj;
      state.feedOnly = false;
      state.eraRange = null;
      state.view = 'all';
      state.limit = 120;
      $$('#topics a').forEach((x) => x.classList.toggle('is-on', x.dataset.topic === state.topic));
      $$('#eras a').forEach((x) => x.classList.remove('is-on'));
      syncNav();
      closeDrawer();
      render();
      return;
    }
    const copy = e.target.closest('[data-copy]');
    if (copy) {
      navigator.clipboard?.writeText(copy.dataset.copy);
      copy.textContent = t('dCopied');
      setTimeout(() => { copy.textContent = t('dCopy'); }, 1200);
    }
  });
}

(function init() {
  wire();
  applyLang();
  load().catch((e) => {
    document.body.insertAdjacentHTML('beforeend',
      `<div class="empty">${esc(t('loadError'))}${esc(e.message)}</div>`);
  });
})();
