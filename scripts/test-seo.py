from pathlib import Path
from lxml import html,etree
import json
D=Path('dist');pages=0;stories=0
for f in D.rglob('*.html'):
 if f.name.startswith('qa'):continue
 d=html.fromstring(f.read_bytes());pages+=1
 assert len(d.xpath('//h1'))==1,str(f)
 assert len(d.xpath('//link[@rel="canonical"]'))==1,str(f)
 data=json.loads(d.xpath('string(//script[@id="site-schema"])'))
 assert data['@context']=='https://schema.org'
 assert any(x['@type']=='Person' and x['sameAs']==['https://www.linkedin.com/in/fazalbinmahmood/','https://www.fiverr.com/sellers/fazalbm'] for x in data['@graph'])
 assert d.xpath('//footer//a[@href="https://www.linkedin.com/in/fazalbinmahmood/"]'),str(f)
 assert 'Website source' not in d.text_content()
 if '-project-story/' in str(f):
  stories+=1;assert d.xpath('string(//link[@rel="canonical"]/@href)').startswith('https://xylosolutions.com/work/')
 for a in d.xpath('//*[@href]'):
  target=a.get('href').split('?')[0].split('#')[0]
  if target.startswith('/'):
   p=D/target.lstrip('/');p=p/'index.html' if target.endswith('/') else p
   assert p.exists(),(f,target)
sitemap=etree.parse(str(D/'sitemap.xml'));urls=sitemap.xpath('//*[local-name()="loc"]/text()')
assert len(urls)==53 and not any('project-story' in x for x in urls)
print(f'PASS: {pages} documents; {stories} republished canonicals; 53 preferred sitemap URLs; profile links, JSON-LD, headings and internal destinations')
