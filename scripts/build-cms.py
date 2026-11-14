from pathlib import Path
from lxml import html,etree
import json,base64,mimetypes
R=Path(__file__).resolve().parents[1];D=R/'dist';assets={};pages=[]
for p in sorted(D.rglob('*')):
 if not p.is_file() or 'server' in p.relative_to(D).parts or p.name.startswith('qa'):continue
 path='/'+str(p.relative_to(D));mime=mimetypes.guess_type(path)[0] or 'application/octet-stream'
 raw=p.read_bytes()
 if p.suffix=='.html':
  doc=html.fromstring(raw);fields=[];route=path[:-10] if path.endswith('index.html') else path
  for el in doc.xpath('//main//*[self::h1 or self::h2 or self::h3 or self::p or self::img or self::a]'):
   if el.xpath('ancestor::nav[@class="breadcrumbs"]'):continue
   if el.tag=='a' and el.xpath('ancestor::h1|ancestor::h2|ancestor::h3|ancestor::p'):continue
   if el.tag!='img' and el.xpath('.//img'):continue
   text=' '.join(el.text_content().split())
   if el.tag!='img' and not text:continue
   key='f'+str(len(fields));el.set('data-cms',key)
   fields.append({'id':key,'kind':'image' if el.tag=='img' else 'link' if el.tag=='a' else 'text','tag':el.tag,'value':el.get('src','') if el.tag=='img' else text,'original':el.get('src','') if el.tag=='img' else text,'href':el.get('href',''),'alt':el.get('alt','')})
  title=doc.xpath('string(//title)').split(' | ')[0];desc=doc.xpath('string(//meta[@name="description"]/@content)')
  if route!='/404.html':pages.append({'canonical':doc.xpath('string(//link[@rel="canonical"]/@href)'),'schema':json.loads(doc.xpath('string(//script[@id="site-schema"])') or '{}'),'path':route,'title':title,'description':desc,'fields':fields,'hidden':False,'new':False,'type':'blog' if route.startswith('/blog/') and '/page/' not in route and route!='/blog/' else 'project' if route.startswith('/projects/') and route!='/projects/' else 'page'})
  raw=etree.tostring(doc,method='html',encoding='utf-8',doctype='<!doctype html>')
 assets[path]={'type':mime,'data':base64.b64encode(raw).decode()}
blog_order={'/blog/'+x['slug']+'/':i for i,x in enumerate(json.loads((D/'assets/blog-index.json').read_text()))}
project_order={'/projects/'+x['slug']+'/':i for i,x in enumerate(json.loads((R/'content/xylo-projects.json').read_text()))}
pages.sort(key=lambda p: (0 if p['type']=='page' else 1 if p['type']=='blog' else 2, blog_order.get(p['path'],project_order.get(p['path'],0))))
seed={'theme':{'headingFont':'Inter Display','bodyFont':'Inter','heroSize':55,'headingSize':36,'bodySize':16,'mobileHeroSize':36,'mobileHeadingSize':30,'accent':'#007e84','soft':'#e8f7f7','text':'#071015','background':'#ffffff','guide':'#07383d','buttonRadius':100},'pages':pages}
(R/'content/cms-seed.json').write_text(json.dumps(seed,ensure_ascii=False))
admin=(R/'admin/index.html').read_text();code=(R/'worker/index.js').read_text()
code=code.replace('/* BUILD_ASSETS */', 'const ASSETS='+json.dumps(assets)+';\nconst SEED='+json.dumps(seed,ensure_ascii=False)+';\nconst ADMIN_HTML='+json.dumps(admin)+';')
out=D/'server';out.mkdir(exist_ok=True);(out/'index.js').write_text(code)
print('CMS build:',len(pages),'editable pages;',len(assets),'assets;',round(len(code)/1024/1024,2),'MB worker')
