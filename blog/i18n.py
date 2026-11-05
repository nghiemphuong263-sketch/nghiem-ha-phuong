"""Generate static Vietnamese pages with matching language links, using stdlib only."""
import json,re
from html import escape
from html.parser import HTMLParser
from pathlib import Path

STYLE='''<style>.language-switch{display:inline-flex;align-items:center;gap:3px;border:1px solid #cbd5db;border-radius:999px;padding:3px;font-size:12px;white-space:nowrap;line-height:1.5}.language-switch a{padding:5px 10px;border-radius:999px}.language-switch a[aria-current]{background:#243b4a;color:white}.nav-inner{height:auto!important;min-height:76px;flex-wrap:wrap;padding-top:12px;padding-bottom:12px}.nav-links{flex-wrap:wrap}@media(max-width:600px){.nav-inner{gap:10px!important}.nav-links{gap:12px!important}.language-switch{font-size:11px}.language-switch a{padding:4px 8px}}</style>'''

def switch(path,vi=False):
 return '<div class="language-switch" aria-label="Language / Ngôn ngữ">'+''.join('<a lang="'+lang+'" hreflang="'+lang+'" href="'+('/vi' if lang=='vi' else '')+path+'"'+(' aria-current="true"' if (lang=='vi')==vi else '')+'>'+label+'</a>' for lang,label in [('en','English'),('vi','Tiếng Việt')])+'</div>'

def alternates(base,path):
 return ''.join(f'<link rel="alternate" hreflang="{lang}" href="{base}{prefix}{path}">' for lang,prefix in [('en',''),('vi','/vi'),('x-default','')])

class Localizer(HTMLParser):
 def __init__(self,d,base):super().__init__(convert_charrefs=True);self.d=d;self.base=base;self.out=[];self.raw=None
 def tr(self,s):
  core=s.strip();return s.replace(core,self.d.get(core,core)) if core else s
 def url(self,s):
  if s.startswith(self.base+'/') and not s.startswith(self.base+'/vi/'):return self.base+'/vi/'+s[len(self.base)+1:]
  if s=='/' or s.startswith('/#') or s.startswith('/blog/'):return '/vi'+s
  return s
 def handle_decl(self,s):self.out.append('<!'+s+'>')
 def handle_starttag(self,tag,attrs):
  result=[];is_schema=tag=='script' and dict(attrs).get('type')=='application/ld+json'
  for k,v in attrs:
   if v is not None:
    if k=='lang' and tag=='html':v='vi'
    elif k in ('href','src'):
     # Assets remain shared. Language-link destinations are already explicit.
     if k=='href' and dict(attrs).get('hreflang'):pass
     else:v=self.url(v) if k=='href' else v
    elif k in ('content','title','alt','placeholder','aria-label'):v=self.tr(v);v=self.url(v) if k=='content' else v
    elif k=='data-search':
     for en,vi in sorted(self.d.items(),key=lambda x:-len(x[0])):v=v.replace(en.lower(),vi.lower())
    if tag=='a' and k=='aria-current' and dict(attrs).get('lang') in ['en','vi']:continue
   result.append(k if v is None else k+'="'+escape(v,quote=True)+'"')
  if tag=='a' and dict(attrs).get('lang')=='vi':result.append('aria-current="true"')
  self.out.append('<'+tag+(' '+' '.join(result) if result else '')+'>')
  if tag in ('script','style'):self.raw='schema' if is_schema else tag
 def handle_startendtag(self,t,a):self.handle_starttag(t,a)
 def handle_endtag(self,t):self.out.append('</'+t+'>');self.raw=None if t in ('script','style') else self.raw
 def handle_data(self,s):
  if self.raw=='schema':
   def walk(v):
    if isinstance(v,dict):return {k:('vi' if k=='inLanguage' else walk(x)) for k,x in v.items()}
    if isinstance(v,list):return [walk(x) for x in v]
    if isinstance(v,str):return self.url(self.tr(v))
    return v
   self.out.append(json.dumps(walk(json.loads(s)),ensure_ascii=False).replace('<','\\u003c'))
  elif self.raw:self.out.append(s)
  else:self.out.append(escape(self.tr(s),quote=False))
 def handle_comment(self,s):self.out.append('<!--'+s+'-->')

def build(root,base):
 d=json.loads((root/'assets/i18n-vi.json').read_text())
 # Fail the build if a new article is missing its essential Vietnamese content.
 for post in json.loads((root/'blog/posts.json').read_text()):
  if post.get('published',True) is False:continue
  required=[post[k] for k in ('title','description','excerpt')]+[post['image']['alt']]+[section['heading'] for section in post['sections']]
  missing=[text for text in required if text not in d or d[text]==text]
  if missing:raise ValueError('Missing Vietnamese translations for '+post['slug']+': '+repr(missing))
 (root/'assets/i18n-vi.js').write_text('window.SITE_VI='+json.dumps(d,ensure_ascii=False)+';\n')
 for f in sorted((root/'blog').rglob('index.html')):
  path='/'+str(f.relative_to(root).parent)+'/'
  en=f.read_text();en=en.replace('</head>',alternates(base,path)+STYLE+'</head>')
  en=en.replace('</nav></div></header>',switch(path)+'</nav></div></header>')
  f.write_text(en)
  p=Localizer(d,base);p.feed(en)
  dest=root/'vi'/f.relative_to(root);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(''.join(p.out))
 # The portfolio is rendered by the same router and dictionary, including dialogs.
 import hashlib
 version=hashlib.sha256((root/'assets/i18n-vi.json').read_bytes()).hexdigest()[:12]
 en=(root/'index.html').read_text()
 en=re.sub(r'/assets/i18n-vi\.js(?:\?v=[^\"]*)?', '/assets/i18n-vi.js?v='+version, en)
 (root/'index.html').write_text(en)
 vi=en.replace('<html lang="en">','<html lang="vi">')
 vi=vi.replace('<head>','<head><base href="/">')
 vi=vi.replace('<title>Nghiêm Hà Phương | Sustainable Finance, Logistics &amp; Operations</title>','<title>'+d.get('Nghiêm Hà Phương | Sustainable Finance, Logistics & Operations','')+'</title>')
 for s in ['Nghiêm Hà Phương | Sustainable Finance, Logistics & Operations','Portfolio of Nghiêm Hà Phương — sustainable finance, carbon markets, logistics, international trade, and operations analysis.']:vi=vi.replace(s,d[s])
 vi=vi.replace('rel="canonical" href="'+base+'/"','rel="canonical" href="'+base+'/vi/"')
 dest=root/'vi/index.html';dest.parent.mkdir(exist_ok=True);dest.write_text(vi)
 sitemap=root/'sitemap.xml';s=sitemap.read_text();locations=re.findall(r'<loc>(.*?)</loc>',s);s=s.replace('</urlset>',''.join('<url><loc>'+url.replace(base+'/',base+'/vi/',1)+'</loc></url>' for url in locations)+'</urlset>');sitemap.write_text(s)
 import xml.etree.ElementTree as ET
 feed=ET.fromstring((root/'blog/feed.xml').read_text())
 for node in feed.iter():
  if node.text:
   text=node.text
   if node.tag=='language':node.text='vi'
   elif node.tag in ('link','guid'):node.text=text.replace(base+'/',base+'/vi/',1)
   else:node.text=d.get(text,text).replace(' — Field notes',' — Ghi chép')
 ET.ElementTree(feed).write(root/'vi/blog/feed.xml',encoding='utf-8',xml_declaration=True)
 print('Built English and Vietnamese versions with matching language links.')
