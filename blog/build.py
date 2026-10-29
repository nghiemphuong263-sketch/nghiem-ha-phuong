"""Build crawlable blog pages from posts.json. Python standard library only."""
import html
import json
import math
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
BASE = 'https://nghiemhaphuongportfolio.netlify.app'
AUTHOR = 'Nghiêm Hà Phương'
CATEGORIES = {
    'sustainable-finance-carbon-markets': 'Sustainable finance & carbon markets',
    'logistics-supply-chain': 'Logistics & supply chain',
    'research-methods': 'Research methods',
    'applied-ai': 'AI & technology',
    'personal-development': 'Personal development',
}
ESC = lambda s: html.escape(str(s), quote=True)


def safe_url(value):
    if not isinstance(value, str) or urlparse(value).scheme != 'https':
        raise ValueError('External links must use HTTPS')
    return ESC(value)


def inline(text, sources):
    text = ESC(text)
    def cite(match):
        i = int(match[1])
        if i < 1 or i > len(sources):
            raise ValueError(f'Citation [{i}] has no source')
        source = sources[i - 1]
        label = ESC(source.get('citeAuthor', source['publisher'])) + ', ' + ESC(source.get('year', 'n.d.'))
        return f'<a class="harvard-citation" href="#source-{i}">({label})</a>'
    return re.sub(r'\[(\d+)\]', cite, text)


def validate(posts):
    slugs = set()
    how_to_weeks = {}
    for p in posts:
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', p['slug']) or p['slug'] in slugs:
            raise ValueError('Invalid or duplicate article slug')
        slugs.add(p['slug'])
        for key in ['title', 'description', 'excerpt', 'answer', 'publishedAt', 'image', 'sections', 'sources']:
            if not p.get(key):
                raise ValueError(f'Missing {key} in {p["slug"]}')
        if p['category'] not in CATEGORIES:
            raise ValueError('Unknown category')
        if p.get('articleType') not in ['how-to', 'research']:
            raise ValueError('Declare articleType: how-to or research')
        if p['articleType'] == 'research' and (not p.get('charts') or not p.get('evidenceAsOf')):
            raise ValueError('Research articles require sourced charts and evidenceAsOf')
        datetime.fromisoformat(p['publishedAt'])
        if datetime.fromisoformat(p['publishedAt']).tzinfo is None:
            raise ValueError('Publication time needs a timezone')
        if p['articleType'] == 'how-to' and p.get('published', True):
            week = tuple(datetime.fromisoformat(p['publishedAt']).astimezone(ZoneInfo('Asia/Ho_Chi_Minh')).isocalendar()[:2])
            how_to_weeks[week] = how_to_weeks.get(week, 0) + 1
            if how_to_weeks[week] > 1:
                raise ValueError('Only one how-to article is allowed per local ISO week')
        image = p['image']
        if urlparse(image['src']).hostname != 'images.pexels.com':
            raise ValueError('Use a verified Pexels photo')
        if urlparse(image['page']).hostname not in ['www.pexels.com', 'pexels.com']:
            raise ValueError('Missing Pexels photo page')
        for key in ['photographer', 'alt', 'page', 'src']:
            if not image.get(key):
                raise ValueError('Incomplete photo attribution')
        for source in p['sources']:
            safe_url(source['url'])
            if not all(source.get(k) for k in ['title', 'publisher', 'author', 'citeAuthor', 'year', 'accessed']):
                raise ValueError('Incomplete source')
        for section in p['sections']:
            if not section.get('heading'):
                raise ValueError('Every section needs a heading')
            for text in section.get('paragraphs', []) + section.get('bullets', []):
                inline(text, p['sources'])
        inline(p['answer'], p['sources'])
        for chart in p.get('charts', []):
            if chart.get('type') not in ['bar', 'line']:
                raise ValueError('Chart must be bar or line')
            if not all(chart.get(k) for k in ['title', 'unit', 'period', 'method', 'sourceIds', 'labels', 'values']):
                raise ValueError('Incomplete chart metadata')
            if not 2 <= len(chart['labels']) <= 12 or len(chart['labels']) != len(chart['values']):
                raise ValueError('Chart requires 2–12 matching labels and values')
            if not all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in chart['values']):
                raise ValueError('Chart values must be finite numbers')
            for i in chart['sourceIds']:
                if not isinstance(i, int) or not 1 <= i <= len(p['sources']):
                    raise ValueError('Chart source is missing')


CSS = '''
:root{--ivory:#f6f3ed;--ink:#18232d;--blue:#287a98;--navy:#243b4a;--slate:#697681;--border:#d9dfe3}*{box-sizing:border-box}body{margin:0;background:var(--ivory);color:var(--ink);font-family:Manrope,system-ui,sans-serif;line-height:1.8}a{color:var(--blue);text-underline-offset:4px}img{max-width:100%;display:block}button,input{font:inherit}.shell{width:min(1160px,calc(100% - 48px));margin:auto}.nav{border-bottom:1px solid var(--border);background:rgba(246,243,237,.97)}.nav-inner{display:flex;justify-content:space-between;align-items:center;gap:24px;min-height:78px}.brand{color:var(--ink);font-weight:800;font-size:19px;text-decoration:none}.nav-links{display:flex;gap:28px;font-size:14px;font-weight:600}.nav-links a{text-decoration:none;color:var(--slate)}.nav-links .active{color:var(--blue)}.eyebrow{text-transform:uppercase;letter-spacing:.13em;color:var(--blue);font-size:11px;font-weight:800}h1,h2,h3{line-height:1.2;letter-spacing:-.035em}h1{font-size:clamp(34px,5vw,62px);max-width:900px;margin:16px 0 24px}h2{font-size:30px}h3{font-size:22px}.intro{padding:70px 0 42px}.intro p{max-width:670px;color:#52616c;font-size:17px}.category-nav{display:flex;gap:10px;flex-wrap:wrap;margin:28px 0 32px}.category-nav a{padding:8px 14px;border:1px solid var(--border);border-radius:30px;font-size:12px;text-decoration:none;color:var(--navy);background:#fff}.category-nav a[aria-current=page]{background:var(--navy);color:#fff;border-color:var(--navy)}.article-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:26px;margin-bottom:64px}.article-card{border:1px solid var(--border);border-radius:16px;overflow:hidden;background:#fff;display:flex;flex-direction:column}.article-card>a{display:block;overflow:hidden}.article-card img{width:100%;aspect-ratio:16/10;object-fit:cover;transition:transform .2s}.article-card:hover img{transform:scale(1.025)}.card-copy{padding:24px;display:flex;flex:1;flex-direction:column}.card-copy h2{font-size:24px;line-height:1.4;margin:12px 0}.card-copy h2 a{color:var(--ink);text-decoration:none}.card-copy p{font-size:14px;color:var(--slate);margin:0 0 20px}.card-copy .read{margin-top:auto;font-weight:700;font-size:13px}.meta{font-size:12px;color:var(--slate)}.featured{display:grid;grid-template-columns:1.05fr 1fr;border:1px solid var(--border);border-radius:20px;overflow:hidden;background:#fff;margin-bottom:48px}.featured .card-copy{padding:36px}.featured h2{font-size:32px}.featured img{width:100%;height:100%;max-height:450px;object-fit:cover}.count{color:var(--slate);font-size:13px}.breadcrumb{font-size:12px;color:var(--slate);padding-top:30px}.article-header{max-width:890px;padding:36px 0 20px}.article-header h1{font-size:clamp(34px,4.4vw,55px)}.article-header .dek{font-size:19px;color:#52616c}.article-image{margin:24px 0 36px}.article-image img{width:100%;aspect-ratio:2/1;object-fit:cover;border-radius:16px}.article-image figcaption{font-size:11px;color:var(--slate);margin-top:8px}.reading-layout{display:grid;grid-template-columns:220px minmax(0,760px);gap:60px;justify-content:center;margin:36px 0 70px}.toc{align-self:start;position:sticky;top:24px;font-size:12px;border-top:2px solid var(--blue);padding-top:16px}.toc strong{font-size:13px}.toc ol{padding-left:18px}.toc li{margin:12px 0}.toc a{color:var(--slate);text-decoration:none}.prose{min-width:0;font-size:17px;line-height:1.9}.prose section{scroll-margin-top:25px}.prose h2{font-size:29px;line-height:1.35;margin:44px 0 18px}.prose p{margin:0 0 22px}.prose li{margin-bottom:12px}.answer{background:#e8f1f3;border-left:3px solid var(--blue);padding:22px 26px;border-radius:0 12px 12px 0}.answer strong{font-size:12px;color:var(--blue);text-transform:uppercase;letter-spacing:.08em}.answer p{margin:8px 0 0}.sources{font-size:14px;border-top:1px solid var(--border);margin-top:42px}.sources li{overflow-wrap:anywhere;padding-bottom:8px}.sources li:target{background:#e8f1f3}.sources a{font-weight:600}.editorial-note{font-size:12px;color:var(--slate);padding:18px 0;border-top:1px solid var(--border)}.author-box{background:#fff;border:1px solid var(--border);padding:24px;border-radius:12px;font-size:13px;margin-top:30px}.related{padding:50px 0;background:#fff;border-top:1px solid var(--border)}.empty{border:1px solid var(--border);padding:36px;border-radius:16px;background:#fff;margin-bottom:70px;max-width:730px}.pager{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:50px}.pager a{background:#fff;border:1px solid var(--border);padding:8px 16px;border-radius:8px}.footer{padding:30px 0;border-top:1px solid var(--border);color:var(--slate);font-size:12px}.footer-inner{display:flex;justify-content:space-between;gap:20px}.skip{position:absolute;left:-10000px}.skip:focus{position:static}a:focus-visible{outline:3px solid var(--blue);outline-offset:4px}sup a{text-decoration:none;font-size:11px;font-weight:800}#search{width:min(100%,400px);border:1px solid var(--border);border-radius:8px;padding:10px 14px;background:#fff;margin:0 0 24px}.hidden{display:none!important}
@media(max-width:980px){.article-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.reading-layout{grid-template-columns:1fr;gap:20px}.toc{position:static;max-width:760px}.featured h2{font-size:27px}}
@media(max-width:640px){.shell{width:calc(100% - 36px)}.nav-inner{flex-wrap:wrap;padding:18px 0;gap:8px}.nav-links{width:100%;gap:20px;font-size:12px}.intro{padding-top:42px}.article-grid,.featured{grid-template-columns:1fr}.featured img{max-height:260px}.featured .card-copy{padding:24px}.article-header{padding-top:22px}.article-header .dek{font-size:17px}.prose{font-size:16px}.prose h2{font-size:25px}.reading-layout{margin-top:20px}.article-image img{aspect-ratio:16/10}.footer-inner{flex-direction:column}.category-nav{gap:8px}.category-nav a{font-size:11px}.article-grid{gap:20px}}
'''
CSS += '''
.harvard-citation{font-size:.92em;white-space:normal}.references{list-style:none;padding-left:0}.references li{padding:10px 0 18px}.data-figure{margin:30px 0;padding:20px;background:#fff;border:1px solid var(--border);border-radius:12px}.data-figure h2{margin-top:0;font-size:23px}.data-figure svg{display:block;width:100%;height:auto}.data-figure figcaption{font-size:12px;line-height:1.7;color:var(--slate)}.data-figure details{font-size:13px;margin-top:15px}.data-figure table{width:100%;border-collapse:collapse;margin-top:12px}.data-figure th,.data-figure td{text-align:left;padding:8px;border-bottom:1px solid var(--border)}.evidence-date{font-size:12px;color:var(--slate)}
'''


def chart_figure(chart, sources, index):
    values, labels = chart['values'], chart['labels']
    low, high = min(0, min(values)), max(0, max(values))
    if low == high:
        high = low + 1
    x0, y0, width, height = 80, 30, 600, 225
    def y(value):
        return y0 + height - (value - low) / (high - low) * height
    spacing = width / len(values)
    marks = ''
    for i in range(5):
        value = low + (high - low) * i / 4
        yy = y(value)
        marks += f'<line x1="{x0}" y1="{yy}" x2="{x0+width}" y2="{yy}" stroke="#e3e8eb"/><text x="{x0-10}" y="{yy+4}" text-anchor="end" font-size="11">{ESC(format(value, ".4g"))}</text>'
    points = []
    for i, (label, value) in enumerate(zip(labels, values)):
        xx = x0 + spacing * (i + .5)
        points.append(f'{xx},{y(value)}')
        if chart['type'] == 'bar':
            top, bottom = min(y(value), y(0)), max(y(value), y(0))
            marks += f'<rect x="{xx-spacing*.3}" y="{top}" width="{spacing*.6}" height="{max(bottom-top, .5)}" fill="#287a98"><title>{ESC(label)}: {ESC(value)} {ESC(chart["unit"])}</title></rect>'
        else:
            marks += f'<circle cx="{xx}" cy="{y(value)}" r="4" fill="#287a98"><title>{ESC(label)}: {ESC(value)} {ESC(chart["unit"])}</title></circle>'
        marks += f'<text x="{xx}" y="{y0+height+23}" text-anchor="middle" font-size="10">{ESC(label)}</text>'
    if chart['type'] == 'line':
        marks += f'<polyline points="{" ".join(points)}" fill="none" stroke="#287a98" stroke-width="2"/>'
    title = ESC(chart['title'])
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 300" role="img" aria-labelledby="chart-title-{index} chart-desc-{index}"><title id="chart-title-{index}">{title}</title><desc id="chart-desc-{index}">Values in {ESC(chart["unit"])}. Full values are in the accompanying data table.</desc><g fill="#52616c" font-family="system-ui,sans-serif">{marks}</g></svg>'
    citations = inline(' '.join('[' + str(i) + ']' for i in chart['sourceIds']), sources)
    table = '<details><summary>View the data table</summary><table><thead><tr><th scope="col">Period or category</th><th scope="col">' + ESC(chart['unit']) + '</th></tr></thead><tbody>' + ''.join('<tr><th scope="row">' + ESC(label) + '</th><td>' + ESC(value) + '</td></tr>' for label, value in zip(labels, values)) + '</tbody></table></details>'
    return f'<figure class="data-figure"><h2>{title}</h2><p class="evidence-date">Unit: {ESC(chart["unit"])} · Data period: {ESC(chart["period"])}</p>{svg}<figcaption>Source: {citations}<br>Method: {ESC(chart["method"])}</figcaption>{table}</figure>'


def write(path, text):
    target = ROOT / path.lstrip('/')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding='utf-8')


def page(title, description, path, body, schema, image=None, article=False):
    url = BASE + path
    image_meta = f'<meta property="og:image" content="{safe_url(image)}"><meta name="twitter:image" content="{safe_url(image)}">' if image else ''
    data = json.dumps(schema, ensure_ascii=False).replace('<', '\\u003c')
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{ESC(title)} | {ESC(AUTHOR)}</title><meta name="description" content="{ESC(description)}"><link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large"><meta property="og:type" content="{'article' if article else 'website'}"><meta property="og:title" content="{ESC(title)}"><meta property="og:description" content="{ESC(description)}"><meta property="og:url" content="{url}"><meta property="og:site_name" content="{ESC(AUTHOR)}"><meta name="twitter:card" content="summary_large_image">{image_meta}
<link rel="alternate" type="application/rss+xml" title="{ESC(AUTHOR)} — Field notes" href="/blog/feed.xml"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet"><style>{CSS}</style><script type="application/ld+json">{data}</script></head>
<body><a class="skip" href="#main">Skip to content</a><header class="nav"><div class="shell nav-inner"><a class="brand" href="/">{ESC(AUTHOR)}</a><nav class="nav-links" aria-label="Main navigation"><a href="/">Home</a><a href="/#/projects">Projects</a><a class="active" href="/blog/">Blog</a><a href="/#/contact">Contact</a></nav></div></header><main id="main">{body}</main><footer class="footer"><div class="shell footer-inner"><span>© {datetime.now().year} {ESC(AUTHOR)} · Field notes</span><span><a href="/blog/editorial-policy/">Editorial approach</a> · <a href="/blog/feed.xml">RSS</a> · <a href="/#/contact">Get in touch</a></span></div></footer></body></html>'''


def reading_time(p):
    words = ' '.join([p['answer']] + [t for s in p['sections'] for t in s.get('paragraphs', []) + s.get('bullets', [])])
    return max(1, math.ceil(len(words.split()) / 220))


def meta(p):
    date = datetime.fromisoformat(p['publishedAt']).strftime('%d %b %Y')
    return f'<time datetime="{ESC(p["publishedAt"])}">{date}</time> · {reading_time(p)} min read'


def card(p, featured=False):
    url = '/blog/' + p['slug'] + '/'
    tag = 'featured' if featured else 'article-card'
    return f'''<article class="{tag}" data-search="{ESC(p['title'] + ' ' + p['excerpt'] + ' ' + CATEGORIES[p['category']]).lower()}"><a href="{url}" aria-label="Read {ESC(p['title'])}"><img src="{safe_url(p['image']['src'])}" alt="{ESC(p['image']['alt'])}" loading="{'eager' if featured else 'lazy'}" width="1200" height="750"></a><div class="card-copy"><span class="eyebrow">{ESC(CATEGORIES[p['category']])}</span><h2><a href="{url}">{ESC(p['title'])}</a></h2><p>{ESC(p['excerpt'])}</p><div class="meta">{meta(p)}</div><a class="read" href="{url}">Read the article →</a></div></article>'''


def category_nav(selected=None):
    all_link = '<a href="/blog/"' + (' aria-current="page"' if not selected else '') + '>All articles</a>'
    return '<nav class="category-nav" aria-label="Browse by topic">' + all_link + ''.join(f'<a href="/blog/category/{slug}/"' + (' aria-current="page"' if slug == selected else '') + f'>{ESC(label)}</a>' for slug, label in CATEGORIES.items()) + '</nav>'


def listing(posts, category=None):
    title = CATEGORIES[category] if category else 'Field notes'
    description = 'Practical perspectives on sustainable finance, supply chains, research, AI and technology and personal development.'
    path = f'/blog/category/{category}/' if category else '/blog/'
    intro = f'<section class="intro"><div class="shell"><div class="eyebrow">The blog · Ideas into practice</div><h1>{ESC(title)}</h1><p>{ESC(description)}</p>{category_nav(category)}</div></section>'
    featured = card(posts[0], True) if posts and not category else ''
    rest = posts[1:] if featured else posts
    content = f'<div class="shell">{featured}'
    if rest:
        content += '<label class="skip" for="search">Search articles</label><input type="search" id="search" placeholder="Search articles on this page…"><div class="article-grid">' + ''.join(card(p) for p in rest) + '</div><p id="no-results" class="hidden">No matching articles.</p>'
        content += '''<script>document.getElementById('search').addEventListener('input',function(){let visible=0;document.querySelectorAll('[data-search]').forEach(card=>{if(card.classList.contains('featured'))return;const match=card.dataset.search.includes(this.value.toLowerCase().trim());card.classList.toggle('hidden',!match);if(match)visible++});document.getElementById('no-results').classList.toggle('hidden',visible>0)});</script>'''
    elif not posts:
        content += '<div class="empty"><h2>A space for the next question.</h2><p>Articles in this topic will appear here as they are published. Explore the other topics in the meantime.</p><a href="/blog/">Browse all articles →</a></div>'
    content += '</div>'
    schema = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': title, 'url': BASE + path, 'description': description, 'mainEntity': {'@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': BASE + '/blog/' + p['slug'] + '/', 'name': p['title']} for i, p in enumerate(posts)]}}
    write(path + 'index.html', page(title, description, path, intro + content, schema, posts[0]['image']['src'] if posts else None))


def article(p, posts):
    path = '/blog/' + p['slug'] + '/'
    sources = p['sources']
    toc = '<aside class="toc"><strong>In this article</strong><ol>' + ''.join(f'<li><a href="#section-{i}">{ESC(s["heading"])}</a></li>' for i, s in enumerate(p['sections'], 1)) + '<li><a href="#sources">Sources</a></li></ol></aside>'
    body = '<div class="shell"><div class="breadcrumb"><a href="/">Home</a> / <a href="/blog/">Blog</a> / ' + ESC(CATEGORIES[p['category']]) + '</div>'
    body += f'<article><header class="article-header"><a class="eyebrow" href="/blog/category/{p["category"]}/">{ESC(CATEGORIES[p["category"]])}</a><h1>{ESC(p["title"])}</h1><p class="dek">{ESC(p["excerpt"])}</p><div class="meta">By <a href="/">{ESC(AUTHOR)}</a> · {meta(p)}</div></header>'
    im = p['image']
    body += f'<figure class="article-image"><img src="{safe_url(im["src"])}" alt="{ESC(im["alt"])}" width="1600" height="800" fetchpriority="high"><figcaption>Illustrative photograph by <a href="{safe_url(im["page"])}" target="_blank" rel="noopener">{ESC(im["photographer"])} on Pexels</a> · <a href="https://www.pexels.com/license/">Pexels License</a></figcaption></figure>'
    body += '<div class="reading-layout">' + toc + '<div class="prose"><div class="answer"><strong>The short answer</strong><p>' + inline(p['answer'], sources) + '</p></div>'
    if p.get('evidenceAsOf'):
        body += '<p class="evidence-date">Evidence checked as of ' + ESC(p['evidenceAsOf']) + '. Data periods are stated separately for each chart.</p>'
    for i, chart in enumerate(p.get('charts', []), 1):
        body += chart_figure(chart, sources, i)
    for i, section in enumerate(p['sections'], 1):
        body += f'<section id="section-{i}"><h2>{ESC(section["heading"])}</h2>'
        body += ''.join('<p>' + inline(text, sources) + '</p>' for text in section.get('paragraphs', []))
        if section.get('bullets'):
            body += '<ul>' + ''.join('<li>' + inline(t, sources) + '</li>' for t in section['bullets']) + '</ul>'
        body += '</section>'
    body += '<section class="sources" id="sources"><h2>References</h2><ol class="references">'
    for i, source in sorted(enumerate(sources, 1), key=lambda item: (item[1]['author'].lower(), str(item[1]['year']), item[1]['title'])):
        body += f'<li id="source-{i}">{ESC(source["author"])} ({ESC(source["year"])}). <em>{ESC(source["title"])}</em>. {ESC(source["publisher"])}. Available at: <a href="{safe_url(source["url"])}" target="_blank" rel="noopener">{ESC(source["url"])}</a> (Accessed: {ESC(source["accessed"])}).</li>'
    body += '</ol></section><p class="editorial-note">Prepared with AI assistance. Source-backed facts are linked; practical frameworks and examples are editorial analysis. Illustrative examples are not reported research findings.</p>'
    body += f'<div class="author-box"><strong>{ESC(AUTHOR)}</strong><p>Exploring sustainable finance, logistics, research and the practical use of AI.</p><a href="/">View portfolio →</a></div></div></div></article></div>'
    related = sorted([x for x in posts if x['slug'] != p['slug']], key=lambda x: x['category'] != p['category'])[:3]
    if related:
        body += '<section class="related"><div class="shell"><h2>Keep exploring</h2><div class="article-grid">' + ''.join(card(x) for x in related) + '</div></div></section>'
    schema = [{'@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': p['title'], 'description': p['description'], 'image': [im['src']], 'datePublished': p['publishedAt'], 'dateModified': p.get('updatedAt', p['publishedAt']), 'author': {'@type': 'Person', 'name': AUTHOR, 'url': BASE + '/'}, 'publisher': {'@type': 'Person', 'name': AUTHOR, 'url': BASE + '/'}, 'mainEntityOfPage': BASE + path, 'inLanguage': 'en', 'articleSection': CATEGORIES[p['category']], 'citation': [x['url'] for x in sources]}, {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': BASE + '/'}, {'@type': 'ListItem', 'position': 2, 'name': 'Blog', 'item': BASE + '/blog/'}, {'@type': 'ListItem', 'position': 3, 'name': p['title'], 'item': BASE + path}]}]
    write(path + 'index.html', page(p['title'], p['description'], path, body, schema, im['src'], True))


def main():
    raw = json.loads((ROOT / 'blog/posts.json').read_text(encoding='utf-8'))
    validate(raw)
    now = datetime.now(ZoneInfo('Asia/Ho_Chi_Minh'))
    posts = sorted([p for p in raw if p.get('published', True) and datetime.fromisoformat(p['publishedAt']) <= now], key=lambda p: p['publishedAt'], reverse=True)
    listing(posts)
    for category in CATEGORIES:
        listing([p for p in posts if p['category'] == category], category)
    for p in posts:
        article(p, posts)
    policy = '<section class="intro"><div class="shell"><div class="eyebrow">Editorial approach</div><h1>Useful ideas, traceable evidence.</h1><div class="prose"><p>Field notes connects research and practical decisions across five topics: sustainable finance and carbon markets, logistics and supply chains, research methods, AI and technology, and personal development.</p><h2>Evidence before certainty</h2><p>Articles link to original research, official documentation and institutional sources where possible. Dates, geography and limits matter. Recommendations and illustrative examples are distinguished from source findings.</p><h2>Research-led, current and measurable</h2><p>The weekly mix is one how-to and six research-led analyses when evidence permits. Analysis articles use verified numerical data, charts and accessible data tables. Observation periods are distinguished from release dates; older background sources are not presented as new developments.</p><h2>Harvard references</h2><p>Sources appear as linked author–date citations, with an alphabetical Harvard reference list. Charts identify their sources, units, data periods and calculations.</p><h2>AI assistance, made visible</h2><p>AI supports research and drafting. It does not replace verification. Articles do not imply firsthand experience, independent experiments or manual author review unless these have actually taken place.</p><h2>Real photographs</h2><p>Article photographs come from Pexels, with a link to the original photo, photographer credit and license. Images illustrate the topic; they are not evidence of a specific event.</p><h2>Corrections</h2><p>If a claim or citation needs correction, <a href="/#/contact">get in touch</a>. Material updates should be recorded with an updated date.</p></div></div></section>'
    write('/blog/editorial-policy/index.html', page('Editorial approach', 'How Field notes uses sources, AI assistance and photography.', '/blog/editorial-policy/', policy, {'@context': 'https://schema.org', '@type': 'WebPage', 'name': 'Editorial approach'}))
    paths = ['/', '/blog/', '/blog/editorial-policy/'] + ['/blog/category/' + c + '/' for c in CATEGORIES]
    sitemap = ''.join('<url><loc>' + BASE + path + '</loc></url>' for path in paths)
    sitemap += ''.join('<url><loc>' + BASE + '/blog/' + p['slug'] + '/</loc><lastmod>' + ESC(p.get('updatedAt', p['publishedAt'])) + '</lastmod></url>' for p in posts)
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + sitemap + '</urlset>')
    write('robots.txt', 'User-agent: *\nAllow: /\n\nSitemap: ' + BASE + '/sitemap.xml\n')
    from email.utils import format_datetime
    items = ''.join('<item><title>' + ESC(p['title']) + '</title><link>' + BASE + '/blog/' + p['slug'] + '/</link><guid isPermaLink="true">' + BASE + '/blog/' + p['slug'] + '/</guid><description>' + ESC(p['excerpt']) + '</description><pubDate>' + format_datetime(datetime.fromisoformat(p['publishedAt'])) + '</pubDate></item>' for p in posts)
    write('/blog/feed.xml', '<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>' + ESC(AUTHOR) + ' — Field notes</title><link>' + BASE + '/blog/</link><description>Research, systems and practical decisions.</description><language>en</language>' + items + '</channel></rss>')
    print(f'Built {len(posts)} articles, 5 topic pages, sitemap and RSS feed.')


if __name__ == '__main__':
    main()
