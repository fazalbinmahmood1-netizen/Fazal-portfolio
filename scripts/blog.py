import json, html, math

def render_blog(root, out, head, nav, footer, search, paths):
    esc=html.escape
    source='https://xylosolutions.com/'
    notes=[
      ('shopify-storefront-design','Shopify Storefront Design: Bringing Structure, Design and Development Together','Custom development works best when the store structure, product information and customer journey are planned together.',[('Start with the shopping experience','Xylo Solutions combines store strategy, conversion-focused design and custom Shopify development. The starting point is the customer: what they need to find, understand and do before buying.'),('Connect the important pages','The homepage introduces the brand, collections help customers explore and product pages explain the details. Treating them as one journey gives the design and development work a shared direction.'),('Build for the team too','Reusable sections and a clear content structure make a storefront easier to maintain. A useful Shopify build supports both the customer experience and the people who update the store.'),('Review before launch','The agency process includes a review of mobile behaviour, performance and the buying journey before launch. Those checks should follow the agreed scope and the features customers will use.')]),
      ('conversion-focused-product-pages','Conversion-Focused Product Pages: Clarity Before Complexity','A closer look at the product information, layout and customer decisions behind conversion-focused storefront design.',[('Understand the hesitation','Xylo Solutions describes conversion optimisation as work on product pages, layouts and the checkout journey. The purpose is to identify the moments where customers hesitate or cannot find what they need.'),('Make the decision easier','A product page needs to communicate the product, its benefits and the next action. The agency’s project stories describe improvements to content hierarchy, product storytelling and calls to action.'),('Treat improvements as testable decisions','A clearer layout is a design objective, not proof of a revenue increase. Agree on what to measure and use the store’s own evidence to assess the change.')]),
      ('planning-shopify-migration','Planning a Shopify Migration: Products, Structure and Search Visibility','A migration involves more than moving a catalogue. Plan the content and customer journey before launch.',[('Map what needs to move','The migration service on Xylo Solutions focuses on product data, site structure and search visibility. Establish what exists on the current store and what needs to be preserved before making changes.'),('Plan the new experience','A platform move is also an opportunity to review navigation and product discovery. Define the customer journey before rebuilding the templates and content.'),('Review the launch path','Product information, links and important customer actions need checking in the new storefront. Redirect planning and a structured review help reduce avoidable disruption.')]),
      ('shopify-seo-foundations','Shopify SEO Foundations: Structure, Content and Technical Detail','How technical and on-page improvements fit into a considered Shopify storefront.',[('Begin with the store itself','Xylo Solutions includes technical and on-page SEO in its service offering. The foundation is a store whose products, collections and important information are easy to understand.'),('Connect content and structure','Page titles, descriptions and internal links should reflect the actual content and the way customers browse. Useful product information supports both shoppers and search visibility.'),('Keep expectations realistic','SEO is ongoing work. Publishing a new design or updating metadata does not guarantee a particular position in search results. Prioritise changes and review their effect over time.')]),
      ('ecommerce-marketing-storefront','Ecommerce Marketing and Your Storefront: Making the Journey Consistent','Connect the promise of a campaign with the product experience customers see after they click.',[('Start with the audience','Xylo Solutions positions ecommerce marketing around attracting relevant visitors and supporting growth. The audience and the reason they visit should inform what the storefront communicates.'),('Keep the message consistent','A campaign and its destination page should tell the same story. Product benefits, photography and the next action need to make sense together.'),('Review the whole journey','Traffic, design and development are connected. Consider the steps from arrival to product discovery and checkout when deciding where to improve the experience.')])
    ]
    articles=[]
    for slug,title,description,sections in notes:
        articles.append(dict(slug=slug,title=title,description=description,image=None,kind='Service notes',source=source,sections=sections))
    project_posts=json.loads((root/'content/xylo-articles.json').read_text())
    stories=[]
    for p in project_posts:
        stories.append(dict(slug=p['slug']+'-project-story',title=p['name']+': An eCommerce Project by Xylo Solutions',description=p['description'],image=p['image'],kind='Project story',source=p['source'],paragraphs=p['paragraphs']))
    # Match the reference's mix of text-led and image-led cards in the opening rows.
    articles=articles[:3]+stories[:1]+articles[3:]+stories[1:]
    def card(a):
        image=f'<img src="{a["image"]}" alt="{esc(a["title"])}" width="1000" height="649" loading="lazy" decoding="async">' if a['image'] else ''
        excerpt='' if image else f'<p>{esc(a["description"])}</p>'
        return f'<article class="blog-card"><a href="/blog/{a["slug"]}/">{image}<h2>{esc(a["title"])}</h2>{excerpt}</a></article>'
    active_nav=nav.replace('href="/blog/"','href="/blog/" aria-current="page"')
    for a in articles:
        route=f'/blog/{a["slug"]}/'
        byline=f'<p class="blog-byline">{a["kind"]} · Xylo Solutions</p>'
        image=f'<img class="article-image" src="{a["image"]}" alt="{esc(a["title"])}" width="1000" height="649">' if a['image'] else ''
        if 'sections' in a:
            body=''.join(f'<h2>{esc(h)}</h2><p>{esc(p)}</p>' for h,p in a['sections'])
            attribution='Adapted from the service approach published by Xylo Solutions.'
        else:
            body='<h2>Project showcase</h2>'+''.join(f'<p>{esc(p)}</p>' for p in a['paragraphs'])
            attribution='Project story originally published by Xylo Solutions.'
        content=head(a['title'],a['description'],route)+active_nav+f'<main id="main" class="article-page"><article class="container article"><a class="back" href="/blog/">← All articles</a>{byline}<h1>{esc(a["title"])}</h1><p class="lead">{esc(a["description"])}</p>{image}{body}<p class="content-note">{attribution} <a href="{a["source"]}">View the source ↗</a></p><a class="button solid" href="/contact/">Discuss your store</a></article></main>'+footer
        f=out/route.strip('/')/'index.html';f.parent.mkdir(parents=True,exist_ok=True);f.write_text(content)
        paths.append(route);search.append({'title':a['title'],'description':a['description'],'url':route})
    count=12;pages=math.ceil(len(articles)/count)
    for n in range(1,pages+1):
        route='/blog/' if n==1 else f'/blog/page/{n}/'
        def page_url(i):return '/blog/' if i==1 else f'/blog/page/{i}/'
        prev=f'<a href="{page_url(n-1)}" rel="prev">« Previous</a>' if n>1 else '<span aria-disabled="true">« Previous</span>'
        nxt=f'<a href="{page_url(n+1)}" rel="next">Next »</a>' if n<pages else '<span aria-disabled="true">Next »</span>'
        nums=''.join(f'<span aria-current="page">{i}</span>' if i==n else f'<a href="{page_url(i)}" aria-label="Page {i}">{i}</a>' for i in range(1,pages+1))
        pagination=f'<nav class="blog-pagination" aria-label="Blog pages">{prev}{nums}{nxt}</nav>'
        intro='Project stories and practical notes on Shopify design, development and the customer experience, drawn from our work at Xylo Solutions.'
        hero=f'<section class="blog-hero"><div class="container blog-hero-grid"><div><h1>eCommerce Blog</h1><p>{intro} Have a question? <a href="/contact/">Get in touch.</a></p></div><form class="blog-search" role="search" action="/blog/" method="get"><label class="visually-hidden" for="blog-query">Search articles</label><input type="search" id="blog-query" name="q" placeholder="Search articles" autocomplete="off"><button class="button solid" type="submit">Search articles</button></form></div></section>'
        cards=''.join(card(a) for a in articles[(n-1)*count:n*count])
        content=head('eCommerce Blog'+(f' · Page {n}' if n>1 else ''),intro,route).replace('<body>','<body class="blog-page">')+active_nav+f'<main id="main">{hero}<section class="blog-list"><div class="container"><p class="blog-results" role="status" aria-live="polite" hidden></p><div class="blog-grid">{cards}</div>{pagination}<noscript><p>Browse all articles using the page links above. Article search requires JavaScript.</p></noscript></div></section></main>'+footer.replace('</body>','<script src="/assets/blog.js" defer></script></body>')
        f=out/route.strip('/')/'index.html';f.parent.mkdir(parents=True,exist_ok=True);f.write_text(content);paths.append(route)
    (out/'assets/blog-index.json').write_text(json.dumps([{k:a.get(k) for k in ('slug','title','description','image')} for a in articles]))
    print(f'Built {len(articles)} blog articles across {pages} listing pages')
