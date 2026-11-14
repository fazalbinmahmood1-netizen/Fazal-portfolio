"""Evidence-based portfolio metadata and editorial additions; no ranking promises."""
from pathlib import Path
from lxml import html, etree
import json
BASE='https://fazalbinmahmood.com'
LINKEDIN='https://www.linkedin.com/in/fazalbinmahmood/'
PERSON={'@type':'Person','@id':BASE+'/#person','name':'Fazal Bin Mahmood','url':BASE+'/about/','jobTitle':'Shopify Designer and Developer','sameAs':[LINKEDIN],'worksFor':{'@id':BASE+'/#organization'}}
ORG={'@type':'Organization','@id':BASE+'/#organization','name':'Xylo Solutions','url':'https://xylosolutions.com/'}
RELATED={
'shopify-development':('shopify-redesign-checklist','A practical Shopify redesign checklist','shopify-storefront-design','Planning a Shopify storefront'),
'shopify-redesign':('shopify-redesign-checklist','A practical Shopify redesign checklist','conversion-focused-product-pages','Clearer product pages'),
'custom-functionality':('personalised-product-flow','Designing a personalised product flow','shopify-storefront-design','Planning the store structure'),
'agency-partnerships':('mobile-store-review','Reviewing a store on mobile','shopify-storefront-design','Storefront planning'),
'conversion-rate-optimisation':('mobile-store-review','Reviewing a store on mobile','conversion-focused-product-pages','Conversion-focused product pages'),
'shopify-migration':('shopify-redesign-checklist','Planning the new storefront','planning-shopify-migration','Planning a Shopify migration'),
'shopify-seo':('store-speed-checklist','A storefront speed checklist','shopify-seo-foundations','Shopify SEO foundations'),
'ecommerce-marketing':('mobile-store-review','Checking the landing experience','ecommerce-marketing-storefront','Connecting campaigns and the storefront')}
DETAILS={
'shopify-development':('What to include in a Shopify development brief','Start with your catalogue, the pages you need and any features your theme cannot already handle. Include examples of the sections your team needs to edit. Identify which requests require an app, which can use Shopify’s existing features, and which need custom development before agreeing on scope.','What should be checked before launch?','Test product variants, sold-out states, cart behaviour and the complete purchase journey. Review the theme on mobile and confirm that your team can update everyday content. A good handover should explain custom sections and any dependencies that need maintenance.'),
'shopify-redesign':('When does a redesign make sense?','A redesign is useful when the current store makes products difficult to understand or the buying journey hard to follow. Start with specific problems: unclear navigation, weak product information, inconsistent layouts or a difficult mobile experience. A new visual style alone does not establish that a store will sell more.','How should success be evaluated?','Agree on the intended improvement before design begins. Compare relevant journeys and conversion data when it is available, allowing for changes in traffic, promotions and stock. Keep valuable URLs and content when possible; plan redirects when a page must move.'),
'custom-functionality':('Plan the complete customer journey','For a personalised product, define the allowed inputs, character limits, preview behaviour and what must appear in the order. Decide how a customer corrects a mistake before adding to cart. A convincing preview is only useful if the final selection is also carried reliably through checkout.','Think about failure states','Check empty inputs, long names, unavailable variants and slow connections. Ensure the feature can be used with a keyboard and on a narrow screen. Document which parts are maintained in the theme and which depend on an app or external service.'),
'agency-partnerships':('Make the design-to-development handoff clear','A useful handoff includes approved desktop and mobile layouts, assets, interaction notes and the editable sections expected in Shopify. Agree who supplies copy, who approves changes and who handles launch access. This reduces ambiguity during implementation.','Agree on review and handover','Define the review stages and the difference between a defect and a new request. Include a final walkthrough of reusable sections, custom functionality and known dependencies. Client communication and responsibility for ongoing maintenance should be agreed before work starts.'),
'conversion-rate-optimisation':('Start with evidence of friction','Review the journey from landing page to product selection, cart and checkout. Look for questions customers cannot answer: which option is right, what delivery costs, when an item arrives and how returns work. Prioritise issues using analytics, customer feedback and direct observation where available.','Avoid confusing a change with a result','A cleaner layout is a design improvement, but an increase in conversion needs measurement. Traffic mix, seasonality, stock and promotions can affect results. Where traffic supports it, compare alternatives with a planned test; otherwise document the limits of a before-and-after comparison.'),
'shopify-migration':('Prepare the migration before moving data','List products, variants, collections, important content and existing URLs. Decide what will be retained, combined or retired. Plan where each valuable old URL should lead and verify that the destination satisfies the same customer need. Keep a backup and an agreed launch checklist.','What needs checking after the move?','Review redirects, internal links, product options and the checkout journey. Check that important pages can be crawled and that the sitemap reflects the new site. Monitor indexing and traffic after launch; migration does not guarantee that rankings will remain unchanged.'),
'shopify-seo':('Give each page a clear purpose','Use collection pages to help shoppers compare a category and product pages to explain a specific item. Write descriptive page titles and useful product information, and connect related pages with understandable links. Avoid repeating keyword variants where a direct explanation would be more helpful.','How will progress be measured?','Use Search Console to understand which searches produce impressions and clicks, which pages are indexed and where errors appear. Separate branded searches from service or product searches. A technical audit score is useful for finding issues, but it does not measure rankings or qualified enquiries.'),
'ecommerce-marketing':('Connect the campaign to the landing page','If a campaign promises a particular product benefit or offer, the destination should make that information easy to find. Check mobile readability, product availability and the next step. Sending more traffic to an unclear page can amplify the same customer experience problem.','Choose measurements before launch','Agree which action matters, how it is recorded and what comparison period is appropriate. Keep the campaign, landing page and checkout experience consistent. Revenue and return-on-ad-spend claims need supporting data; they should not be inferred from a redesign alone.')}
def append(parent,markup):parent.append(html.fragment_fromstring(markup,create_parent='section'))
def enhance(D):
 canonical_paths=[]
 for file in D.rglob('*.html'):
  if file.name.startswith('qa'):continue
  route='/'+str(file.relative_to(D));route=route[:-10] if route.endswith('index.html') else route
  doc=html.fromstring(file.read_bytes());head=doc.find('head');main=doc.find('.//main');article=doc.find('.//main/article')
  title=doc.xpath('string(//title)').split(' | ')[0];desc=doc.xpath('string(//meta[@name="description"]/@content)');canonical=BASE+route
  story=route.startswith('/blog/') and route.endswith('-project-story/')
  if story:canonical='https://xylosolutions.com/work/'+route.split('/')[2].removesuffix('-project-story')
  for el in doc.xpath('//link[@rel="canonical"]|//meta[@property="og:url"]'):el.set('href' if el.tag=='link' else 'content',canonical)
  if not story and route!='/404.html':canonical_paths.append(route)
  # Social links are normal anchors; no third-party widgets or scripts.
  footer=doc.xpath('//footer//div[contains(@class,"footer-grid")]/div')[0]
  append(footer,f'<div class="profile-links" aria-label="Fazal’s professional profiles"><a class="profile-button" rel="me" href="{LINKEDIN}"><span class="profile-icon" aria-hidden="true">in</span>Connect with Fazal<span aria-hidden="true">↗</span></a></div>')
  if route=='/about/' and article is not None:
   append(article,f'<div class="editorial-addition"><h2>Shopify design with a practical development focus</h2><p>I’m based in Lahore, Pakistan, and lead Xylo Solutions. My work connects the visual design of a store with how customers find products, choose options and move towards checkout. You can explore the agency projects featured here and the practical guides that explain the approach.</p><p>For storefront projects, start with <a href="/services/shopify-development/">Shopify development</a> or <a href="/services/shopify-redesign/">Shopify redesign</a>. For personalised products, see <a href="/services/custom-functionality/">custom Shopify functionality</a>.</p><h2>Connect with me</h2><p>Find my professional background and updates on my personal LinkedIn profile.</p><a class="profile-button" rel="me" href="{LINKEDIN}"><span class="profile-icon" aria-hidden="true">in</span>Fazal on LinkedIn<span aria-hidden="true">↗</span></a></div>')
  slug=route.strip('/').split('/')[-1]
  if route.startswith('/services/') and slug in DETAILS and article is not None:
   h,p,h2,p2=DETAILS[slug];g,gt,b,bt=RELATED[slug]
   append(article,f'<div class="editorial-addition"><h2>{h}</h2><p>{p}</p><h2>{h2}</h2><p>{p2}</p><h2>Useful reading before your project</h2><ul><li><a href="/guides/{g}/">{gt}</a></li><li><a href="/blog/{b}/">{bt}</a></li><li><a href="/projects/">Explore Xylo Solutions projects</a></li></ul><p>Work with <a href="/about/">Fazal Bin Mahmood</a>, founder of Xylo Solutions, to define the scope for your store.</p></div>')
  is_article=(route.startswith('/blog/') and route!='/blog/' and '/page/' not in route) or (route.startswith('/guides/') and route!='/guides/')
  if is_article and article is not None:
   author='Xylo Solutions' if route.startswith('/blog/') else 'Fazal Bin Mahmood';url='https://xylosolutions.com/about' if author=='Xylo Solutions' else '/about/'
   append(article,f'<aside class="author-note"><strong>About the author</strong><p><a href="{url}">{author}</a> · Shopify design and development.</p><p>Explore <a href="/services/shopify-development/">Shopify development services</a> or <a href="/guides/">more practical eCommerce guides</a>.</p></aside>')
  if article is not None:
   parent='/blog/' if route.startswith('/blog/') else '/projects/' if route.startswith('/projects/') else '/guides/' if route.startswith('/guides/') else None
   crumbs=[('Home','/')]
   if parent and parent!=route:crumbs.append(({'/blog/':'Blog','/projects/':'Projects','/guides/':'Guides'}[parent],parent))
   crumbs.append((title,route));nav=html.Element('nav',attrib={'class':'breadcrumbs','aria-label':'Breadcrumb'})
   for i,(label,url) in enumerate(crumbs):
    el=etree.SubElement(nav,'span' if i==len(crumbs)-1 else 'a');el.text=label
    if el.tag=='a':el.set('href',url)
    else:el.set('aria-current','page')
   main.insert(0,nav)
  else:crumbs=[]
  graph=[PERSON,ORG,{'@type':'WebSite','@id':BASE+'/#website','name':'Fazal Bin Mahmood','url':BASE+'/','publisher':{'@id':BASE+'/#person'}}]
  page={'@type':'ProfilePage' if route=='/about/' else 'WebPage','@id':BASE+route+'#webpage','url':canonical,'name':title,'description':desc,'isPartOf':{'@id':BASE+'/#website'},'inLanguage':'en'}
  if route=='/about/':page['mainEntity']={'@id':BASE+'/#person'}
  graph.append(page)
  if is_article:
   a={'@type':'BlogPosting' if route.startswith('/blog/') else 'Article','headline':title,'description':desc,'mainEntityOfPage':canonical,'author':{'@id':BASE+('/#organization' if route.startswith('/blog/') else '/#person')},'publisher':{'@id':BASE+'/#person'}}
   img=doc.xpath('//main//img/@src')
   if img:a['image']=BASE+img[0] if img[0].startswith('/') else img[0]
   graph.append(a)
   for el in doc.xpath('//meta[@property="og:type"]'):el.set('content','article')
  if crumbs:graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i+1,'name':name,'item':BASE+url} for i,(name,url) in enumerate(crumbs)]})
  script=etree.SubElement(head,'script',attrib={'type':'application/ld+json','id':'site-schema'});script.text=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<','\\u003c')
  etree.SubElement(head,'meta',attrib={'name':'twitter:card','content':'summary'})
  if route=='/404.html':etree.SubElement(head,'meta',attrib={'name':'robots','content':'noindex'})
  file.write_bytes(etree.tostring(doc,method='html',encoding='utf-8',doctype='<!doctype html>'))
 (D/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{BASE}{p}</loc></url>' for p in sorted(canonical_paths))+'</urlset>')
