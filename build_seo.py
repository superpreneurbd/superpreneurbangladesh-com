#!/usr/bin/env python3
"""SEO rebuild: 8 pages on the verified keyword map (2026-10-06).
Keeps the TPH-derived design system from build.py; retargets titles/metas/H1s,
adds FAQPage + VideoObject + Person JSON-LD, hub-spoke internal links,
2 new pages (Fiverr guide, income-sites guide), entity alignment."""
import re, html as htmllib
import build
from build import (page, footer, NEWSLETTER, PAGES, URI, THUMB,
                   extract_body, FONTS)

# ---------- extended image sets (new thumbs generated for the 2 new pages) ----------
import base64 as _b64
for _k in ['fiverr-guide', 'income-sites']:
    try:
        THUMB[_k] = 'data:image/webp;base64,' + _b64.b64encode(
            open(f'assets_uri/thumb_{_k}.webp', 'rb').read()).decode()
        URI[_k] = 'data:image/webp;base64,' + _b64.b64encode(
            open(f'assets_uri/{_k}.webp', 'rb').read()).decode()
    except FileNotFoundError:
        pass  # fallback handled below

NAV_SEO = [
    ('index.html', 'Home'),
    ('online-income-sites-bangladesh.html', 'Income Sites'),
    ('fiverr-bangladesh.html', 'Fiverr Guide'),
    ('freelancing-bangladesh.html', 'Freelancing Guide'),
    ('getting-paid.html', 'Getting Paid'),
    ('uk-bangladeshi-freelancers.html', 'UK Bangladeshis'),
    ('hire-bangladeshi-talent.html', 'Hire Talent'),
    ('about.html', 'About'),
]
build.NAV = NAV_SEO
from build import header  # noqa: E402  (picks up patched NAV)

# ---------- keyword-targeted metadata ----------
META = {
 'index.html': dict(
    title='Online Income in Bangladesh: Practical English Guides to Earning Online (2026)',
    desc='Honest English guides on online income in Bangladesh — freelancing, Fiverr, getting paid via Payoneer and Wise. For Bangladeshis building a second income, wherever they live.',
    tag='START HERE', h1='Online Income in Bangladesh: Practical Guides to Earning Online in 2026'),
 'online-income-sites-bangladesh.html': dict(
    title='Online Income Sites in Bangladesh: 7 Legit Ways to Earn Online (2026)',
    desc='Which online income sites in Bangladesh actually pay? Honest 2026 review of Fiverr, Upwork, Freelancer.com and more — plus the scam red flags to avoid.',
    tag='GUIDES', img='income-sites', imgalt='Laptop showing freelance marketplace websites with Bangladeshi taka notes beside it',
    h1='Online Income Sites in Bangladesh: 7 Legit Ways to Earn (2026)'),
 'fiverr-bangladesh.html': dict(
    title='Fiverr in Bangladesh: The Complete Beginner\u2019s Guide to Getting Started (2026)',
    desc='How to start on Fiverr from Bangladesh: account setup, gig creation, pricing, getting your first order and withdrawing earnings via Payoneer.',
    tag='GUIDES', img='fiverr-guide', imgalt='Freelancer creating a Fiverr gig on a laptop in a home office in Dhaka',
    h1='Fiverr in Bangladesh: The Complete Beginner\u2019s Guide (2026)'),
 'freelancing-bangladesh.html': dict(
    title='Freelancing in Bangladesh: How to Start and Get Your First Client (2026)',
    desc='How to start freelancing in Bangladesh: beginner skills, Fiverr and Upwork setup, pricing in BDT, and getting paid via Payoneer or Wise.',
    tag='GUIDES', img='freelancing-guide', imgalt='Freelancer working on a laptop showing a freelance marketplace profile',
    h1='Freelancing in Bangladesh: How to Start and Get Your First Client (2026)'),
 'getting-paid.html': dict(
    title='Payoneer Bangladesh: How Freelancers Receive Money from Abroad (2026)',
    desc='Payoneer in Bangladesh explained: account setup, withdrawing to local banks and bKash, fees, plus how Wise compares for freelancers.',
    tag='MONEY', img='getting-paid', imgalt='Hand holding a phone with a mobile banking payment confirmation, laptop and banknotes on desk',
    h1='Payoneer Bangladesh: How Freelancers Receive Money from Abroad (2026)'),
 'uk-bangladeshi-freelancers.html': dict(
    title='Freelancing for Bangladeshis in the UK: Payments, Tax & Finding Clients (2026)',
    desc='A practical guide for Bangladeshis in the UK: freelancing legally, getting paid, tax basics and finding clients.',
    tag='DIASPORA', img='uk-freelancers', imgalt='Bangladeshi professional with laptop near the London skyline at dusk',
    h1='Freelancing for Bangladeshis in the UK (2026)'),
 'hire-bangladeshi-talent.html': dict(
    title='Hire Bangladeshi Freelancers & Digital Marketers | Expert Asset Studio',
    desc='Skilled execution for your client work — ads, landing pages, video, copy and SEO — handled behind the scenes from Dhaka.',
    tag='FOR BUSINESS', img='hire-talent', imgalt='Bangladeshi digital marketing team reviewing campaign dashboards in a Dhaka office',
    h1='Hire Bangladeshi Freelancers & Digital Marketers'),
 'about.html': dict(
    title='About Imtiaz Khan — Founder of Superpreneur Bangladesh',
    desc='Imtiaz Khan is a digital marketer from Dhaka: founder of Superpreneur Bangladesh and Expert Asset Studio. Read the story and the mission.',
    tag='ABOUT', imgalt='About Superpreneur Bangladesh',
    h1='About Imtiaz Khan & Superpreneur Bangladesh'),
}

# video embeds: page -> (youtube_id, title)
VIDEOS = {
    'index.html': ('JRN5px0PTi4', 'Online income in Bangladesh — watch the breakdown'),
    'freelancing-bangladesh.html': ('VUsEubXVpcE', 'AI tools for freelancers and entrepreneurs'),
}

def page_seo(title, desc, active, body_html, extra_head=''):
    # homepage canonical is the root URL (sitemap uses root, not /index.html)
    canon = 'https://superpreneurbangladesh.com/' if active == 'index.html' else f'https://superpreneurbangladesh.com/{active}'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<link rel="stylesheet" href="style.css">
{FONTS}
{extra_head}</head>
<body>
{header(active)}
{body_html}
{footer()}
</body>
</html>'''

def faq_jsonld(body_html):
    """Build FAQPage JSON-LD from the page's own <details class=faq-item> blocks."""
    import json
    items = re.findall(
        r'<details class="faq-item"[^>]*>\s*<summary>(.*?)</summary>\s*<div class="faq-a">(.*?)</div>',
        body_html, re.S)
    if not items:
        return ''
    def clean(s):
        s = re.sub(r'<[^>]+>', '', s)
        return htmllib.unescape(s).strip()
    qs = [{"@type": "Question", "name": clean(q),
           "acceptedAnswer": {"@type": "Answer", "text": clean(a)}}
          for q, a in items]
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": qs}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>'

def video_block(vid, vtitle, page_url):
    embed = f'''<div class="video-embed" style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:8px;margin:28px 0;">
  <iframe src="https://www.youtube.com/embed/{vid}" title="{htmllib.escape(vtitle)}"
    style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    allowfullscreen loading="lazy"></iframe></div>'''
    import json
    vo = {"@context": "https://schema.org", "@type": "VideoObject",
          "name": vtitle, "description": vtitle + " — Superpreneur Bangladesh",
          "thumbnailUrl": f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg",
          "embedUrl": f"https://www.youtube.com/embed/{vid}",
          "contentUrl": f"https://www.youtube.com/watch?v={vid}"}
    return embed, '<script type="application/ld+json">' + json.dumps(vo, ensure_ascii=False) + '</script>'

PERSON_JSONLD = '''<script type="application/ld+json">{"@context":"https://schema.org","@type":"Person",
"name":"Imtiaz Khan","jobTitle":"Founder, Superpreneur Bangladesh",
"description":"Digital marketer from Dhaka, Bangladesh. Founder of Superpreneur Bangladesh and Expert Asset Studio.",
"url":"https://superpreneurbangladesh.com/about.html",
"sameAs":["https://www.youtube.com/@superpreneurbd","https://superpreneur.bd","https://imtiazkhan.top"]}</script>'''

def card_seo(u):
    meta = META[u]
    tkey = {'online-income-sites-bangladesh.html': 'income-sites',
            'fiverr-bangladesh.html': 'fiverr-guide',
            'freelancing-bangladesh.html': 'freelancing-guide',
            'getting-paid.html': 'getting-paid',
            'uk-bangladeshi-freelancers.html': 'uk-freelancers',
            'hire-bangladeshi-talent.html': 'hire-talent'}.get(u)
    src = THUMB.get(tkey) or THUMB['freelancing-guide']
    return f'''<div class="card">
  <a href="{u}"><img src="{src}" alt="{htmllib.escape(meta['imgalt'])}" loading="lazy"></a>
  <span class="tag">{meta['tag']}</span>
  <h3><a href="{u}">{htmllib.escape(meta['h1'].split(' (')[0])}</a></h3>
  <span class="byline-sm">OCTOBER 2026 &nbsp;·&nbsp; <b>IMTIAZ KHAN</b></span>
</div>'''

def rel_grid_seo(exclude):
    order = ['online-income-sites-bangladesh.html', 'fiverr-bangladesh.html',
             'freelancing-bangladesh.html', 'getting-paid.html',
             'uk-bangladeshi-freelancers.html', 'hire-bangladeshi-talent.html']
    cards = ''.join(card_seo(u) for u in order if u != exclude)
    return f'''<h2 class="sec-head it">You May Also Like</h2><div class="spacer"></div>
<div class="rel-grid">{cards}</div>'''

def pick_row_seo(u):
    meta = META[u]
    tkey = {'online-income-sites-bangladesh.html': 'income-sites',
            'fiverr-bangladesh.html': 'fiverr-guide',
            'freelancing-bangladesh.html': 'freelancing-guide',
            'getting-paid.html': 'getting-paid',
            'uk-bangladeshi-freelancers.html': 'uk-freelancers',
            'hire-bangladeshi-talent.html': 'hire-talent'}.get(u)
    img = f'<a href="{u}"><img src="{THUMB.get(tkey) or THUMB["freelancing-guide"]}" alt="{htmllib.escape(meta["imgalt"])}" loading="lazy"></a>' if tkey else ''
    title = htmllib.escape(meta['h1'].split(' (')[0])
    return f'''<div class="pick-row">{img}
  <div><h4><a href="{u}">{title}</a></h4>
  <span class="byline-sm">OCTOBER 2026 &nbsp;·&nbsp; <b>IMTIAZ KHAN</b></span></div>
</div>'''

def article_shell(fname, body_inner):
    """Wrap an article body with hero/byline/disclosure/newsletter/rel-grid."""
    meta = META[fname]
    if 'cta-band' in body_inner:
        body_inner = body_inner.replace('<div class="cta-band">', NEWSLETTER + '\n<div class="cta-band">', 1)
    else:
        body_inner += '\n' + NEWSLETTER
    hero = ''
    if meta.get('img') and URI.get(meta['img']):
        hero = (f'<figure class="hero-img"><img src="{URI[meta["img"]]}" '
                f'alt="{htmllib.escape(meta["imgalt"])}" loading="eager"></figure>')
    return f'''<div class="wrap">
  <div class="crumbs">SEE MORE FROM <a href="index.html#guides">{meta['tag']}</a></div>
  <h1 class="article-h1">{htmllib.escape(meta['h1'])}</h1>
  <div class="byline">
    <div class="avatar">IK</div>
    <div class="who"><b>by <a href="about.html">Imtiaz Khan</a></b><br><span class="role">Founder, Superpreneur Bangladesh</span></div>
    <div class="updated">Updated October 2026</div>
  </div>
  {hero}
  <div class="disclosure">Free guides, no hype. We fund this site through our own ebooks, courses and services — never paid placements.</div>
  <div class="article-body">
{body_inner}
  </div>
  {rel_grid_seo(fname)}
</div>'''

# ---------------- body extraction from built files ----------------
def strip_div_class(html, classname):
    """Remove <div class="classname">...</div> blocks, nesting-aware."""
    out, i, n = [], 0, len(html)
    pat = f'<div class="{classname}"'
    while i < n:
        j = html.find(pat, i)
        if j == -1:
            out.append(html[i:])
            break
        out.append(html[i:j])
        depth, k = 1, html.find('>', j) + 1
        while depth and k < n:
            nxt_open, nxt_close = html.find('<div', k), html.find('</div>', k)
            if nxt_open != -1 and nxt_open < nxt_close:
                depth += 1
                k = html.find('>', nxt_open) + 1
            else:
                depth -= 1
                k = nxt_close + 6
        i = k
    return ''.join(out)

def extract_built_body(fname):
    html = open(fname, encoding='utf-8').read()
    m = re.search(r'<div class="article-body">\n(.*?)\n  </div>\s*<h2 class="sec-head it">You May Also Like',
                  html, re.S)
    assert m, fname
    body = strip_div_class(m.group(1), 'news-panel')
    return body.strip()

# ---------------- new homepage ----------------
def build_index():
    feat = META['online-income-sites-bangladesh.html']
    vid, vtitle = VIDEOS['index.html']
    v_embed, v_jsonld = video_block(vid, vtitle, 'https://superpreneurbangladesh.com/')
    body = f'''<div class="wrap">
  <section class="masthead"><div class="mast-grid">
    <div class="mast-feature-img"><a href="online-income-sites-bangladesh.html"><img src="{THUMB['hero-home']}" alt="Bangladeshi freelancer earning online income from a home desk with Dhaka skyline outside the window" loading="eager"></a></div>
    <div class="mast-feature">
      <span class="tag">START HERE</span>
      <h1><a href="online-income-sites-bangladesh.html">Online Income in Bangladesh: Practical Guides to Earning Online in 2026</a></h1>
      <p class="mast-sub">Honest, practical English guides on freelancing, Fiverr, and getting paid via Payoneer and Wise — for Bangladeshis building a second income after office hours, wherever they live.</p>
      <span class="byline-sm">OCTOBER 2026 &nbsp;·&nbsp; <b>IMTIAZ KHAN</b></span>
    </div>
    <div class="rail-card">
      <h3>Free Freelancing Starter Checklist</h3>
      <p>The exact first 10 steps to take before you chase clients. One email, no spam.</p>
      <form onsubmit="location.href='mailto:superpreneurbangladesh@gmail.com?subject=Free Checklist Request&body=Please send me the Freelancing Starter Checklist. My email: '+encodeURIComponent(this.email.value);return false;">
      <input type="email" name="email" placeholder="Your email address" required aria-label="Email address">
      <button type="submit">Send Me the Checklist</button>
    </form>
      <small>We respect your inbox. Unsubscribe anytime.</small>
    </div>
  </div></section>

  <div class="duo">
    <div>
      <h2 class="sec-head it">Editor's Picks</h2><div class="spacer"></div>
      {pick_row_seo('fiverr-bangladesh.html')}
      {pick_row_seo('freelancing-bangladesh.html')}
    </div>
    <div>
      <h2 class="sec-head it">Trending</h2><div class="spacer"></div>
      {pick_row_seo('getting-paid.html')}
      {pick_row_seo('online-income-sites-bangladesh.html')}
    </div>
  </div>

  <h2 class="sec-head" id="guides">Our Guides</h2>
  <div class="cards">
    {card_seo('online-income-sites-bangladesh.html')}
    {card_seo('fiverr-bangladesh.html')}
    {card_seo('freelancing-bangladesh.html')}
    {card_seo('getting-paid.html')}
    {card_seo('uk-bangladeshi-freelancers.html')}
    {card_seo('hire-bangladeshi-talent.html')}
  </div>

  <div class="vblock">
    <h2 class="sec-head">Watch: Online Income Explained</h2>
    {v_embed}
    <p style="text-align:center;max-width:640px;margin:0 auto;">The video companion to these guides — from the <a href="https://www.youtube.com/@superpreneurbd">Superpreneur Bangladesh YouTube channel</a>.</p>
  </div>

  <div class="vblock">
    <h2 class="sec-head">Start Here</h2>
    <div class="vblock-grid">
      <div class="vblock-feat">
        <a href="freelancing-bangladesh.html"><img src="{THUMB['freelancing-guide']}" alt="{htmllib.escape(META['freelancing-bangladesh.html']['imgalt'])}" loading="lazy"></a>
        <h3><a href="freelancing-bangladesh.html">{htmllib.escape(META['freelancing-bangladesh.html']['h1'])}</a></h3>
        <div style="text-align:center"><span class="byline-sm">OCTOBER 2026 &nbsp;·&nbsp; <b>IMTIAZ KHAN</b></span></div>
      </div>
      <div>
        {pick_row_seo('getting-paid.html')}
        {pick_row_seo('uk-bangladeshi-freelancers.html')}
        {pick_row_seo('hire-bangladeshi-talent.html')}
      </div>
    </div>
  </div>
  <div style="text-align:center"><a class="loadmore" href="#guides" style="display:inline-block">Browse All Guides</a></div>
</div>'''
    meta = META['index.html']
    out = page_seo(meta['title'], meta['desc'], 'index.html', body, extra_head=v_jsonld)
    open('index.html', 'w', encoding='utf-8').write(out)
    print('built index.html', len(out))

# ---------------- about with entity schema ----------------
def build_about():
    body_inner = extract_built_body('about.html')
    content = f'''<div class="wrap">
  <div class="crumbs">SEE MORE FROM <a href="index.html">SUPERPRENEUR BANGLADESH</a></div>
  <h1 class="article-h1">About Imtiaz Khan &amp; Superpreneur Bangladesh</h1>
  <div class="byline">
    <div class="avatar">IK</div>
    <div class="who"><b>by <a href="about.html">Imtiaz Khan</a></b><br><span class="role">Founder, Superpreneur Bangladesh</span></div>
    <div class="updated">Updated October 2026</div>
  </div>
  <div class="disclosure">Free guides, no hype. We fund this site through our own ebooks, courses and services — never paid placements.</div>
  <div class="article-body">
{body_inner}
{NEWSLETTER}
  </div>
  {rel_grid_seo('about.html')}
</div>'''
    meta = META['about.html']
    out = page_seo(meta['title'], meta['desc'], 'about.html', content, extra_head=PERSON_JSONLD)
    open('about.html', 'w', encoding='utf-8').write(out)
    print('built about.html', len(out))

# ---------------- articles ----------------
def build_existing(fname):
    body = extract_built_body(fname)
    # strip previously-inserted video embeds so regeneration is idempotent
    # (the Oct 6 build duplicated the embed by re-running on built files)
    body = re.sub(r'<div class="video-embed".*?</div>\s*', '', body, flags=re.S)
    extra = ''
    if fname in VIDEOS:
        vid, vtitle = VIDEOS[fname]
        v_embed, v_jsonld = video_block(vid, vtitle,
                                        f'https://superpreneurbangladesh.com/{fname}')
        body = body.replace('<h2>Frequently asked questions</h2>',
                            v_embed + '\n<h2>Frequently asked questions</h2>', 1)
        extra += v_jsonld
    extra += faq_jsonld(body)
    meta = META[fname]
    out = page_seo(meta['title'], meta['desc'], fname, article_shell(fname, body),
                   extra_head=extra)
    open(fname, 'w', encoding='utf-8').write(out)
    print('built', fname, len(out))

def build_new(fname, body_raw):
    extra = faq_jsonld(body_raw)
    meta = META[fname]
    out = page_seo(meta['title'], meta['desc'], fname, article_shell(fname, body_raw),
                   extra_head=extra)
    open(fname, 'w', encoding='utf-8').write(out)
    print('built', fname, len(out))

# ---------------- sitemap ----------------
def build_sitemap():
    urls = ['index.html', 'online-income-sites-bangladesh.html', 'fiverr-bangladesh.html',
            'freelancing-bangladesh.html', 'getting-paid.html',
            'uk-bangladeshi-freelancers.html', 'hire-bangladeshi-talent.html', 'about.html']
    entries = '\n'.join(
        f'  <url><loc>https://superpreneurbangladesh.com/{u.replace("index.html", "")}</loc>'
        f'<lastmod>2026-10-07</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>'
        for u in urls)
    xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}\n</urlset>'
    open('sitemap.xml', 'w', encoding='utf-8').write(xml)
    print('built sitemap.xml')

if __name__ == '__main__':
    from build_seo_bodies import FIVERR_BODY, INCOME_SITES_BODY
    build_index()
    build_new('fiverr-bangladesh.html', FIVERR_BODY.strip())
    build_new('online-income-sites-bangladesh.html', INCOME_SITES_BODY.strip())
    for f in ['freelancing-bangladesh.html', 'getting-paid.html',
              'uk-bangladeshi-freelancers.html', 'hire-bangladeshi-talent.html']:
        build_existing(f)
    build_about()
    build_sitemap()
    print('SEO rebuild done')
