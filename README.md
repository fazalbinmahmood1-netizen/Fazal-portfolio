# Fazal Bin Mahmood portfolio

A custom, static website using semantic HTML, CSS and vanilla JavaScript. No npm dependencies, runtime AI API, database or paid builder.

## Files

- `dist/`: ready-to-host website, including all HTML pages, styles, JavaScript and graphics.
- `scripts/build.py`: Python 3 standard-library generator for shared navigation, footer, content pages, search data and sitemap.
- `dist/assets/style.css`: responsive layouts and motion.
- `dist/assets/app.js`: menu, search dialog, scroll reveals and carousel.

## Local preview

Run `python3 -m http.server 8080 --directory dist` and open http://localhost:8080.

To regenerate the HTML after editing page content: `python3 scripts/build.py`. CSS and JavaScript are maintained directly under `dist/assets/` and are not overwritten by this command.

## Cloudflare Pages deployment

1. In your Cloudflare account, create a Pages project and connect this GitHub repository.
2. Select branch `main`.
3. Framework preset: None. Build command: leave empty. Output directory: `dist`.
4. Deploy, then add `fazalbinmahmood.com` through the project's Custom domains section.
5. Follow Cloudflare's DNS instructions for the domain. Configure the preferred www redirect if you use www.

The generated files are committed, so Python is not required in Cloudflare. Git pushes trigger a new deployment once the Git integration is connected. No Cloudflare account or custom domain has been connected by this repository commit.

## Content and launch status

This is a review version, not a verified pixel-perfect copy. It follows the supplied reference's black/white/blush section structure, Jost typography, outlined buttons, project grid, quote bubble and guide cards. Copy and branding are adapted to Fazal. The header uses a personal text wordmark; the official agency logo appears in the founder section and footer. Portfolio content and 28 optimised WebP covers were imported from Xylo Solutions with source links recorded in content/xylo-projects.json. The homepage features six projects and the project index lists all 28. The placeholder testimonial section is replaced with the agency’s four-step process; no client testimonials are invented. The agency logo and cyan/teal palette are used while retaining the personal site layout. Contact uses the published company email, address and contact page. No local contact form or newsletter service is configured. Guides are initial editorial drafts, not researched traffic guarantees.

The static site has no admin panel or server-side backend. Content is edited in GitHub/the source files. Search runs in the visitor's browser. Fonts currently load from Google Fonts' font CDN, using `font-display: swap`; no analytics or tracking scripts are included.

## SEO

Each page includes a title, description, canonical URL and basic Open Graph metadata. A sitemap and robots.txt target https://fazalbinmahmood.com. Use a preview deployment for review; finish content before connecting the production domain. Search rankings are not guaranteed.

## Validation

JavaScript syntax and local internal link/asset integrity are checked. Browser QA covers desktop rendering, local search, carousel selection, and mobile/tablet iframe layouts. This does not substitute for testing on physical iOS and Android devices.

## Xylo content update

Source: https://xylosolutions.com/ and https://xylosolutions.com/work (reviewed 13 November 2026). Agency projects are attributed to Xylo Solutions, not claimed as solo work. Conflicting experience/team figures on the source site are omitted. The original layout and Jost typeface are retained; brand colour accents and agency assets match Xylo. Update project copy in `content/xylo-projects.json` and run the generator.

## Blog

The /blog/ listing follows a four-column editorial card layout with responsive mobile styles, 33 articles, three paginated pages and client-side article search. Content includes 28 Xylo project stories imported in content/xylo-articles.json and five adapted service notes. Each article links to its source. No newsletter subscription service is connected. Rebuild with python scripts/build.py.

## Agency typography and reference layout

Uses Xylo’s Inter and Inter Display font-face sources, with measured desktop typography (55px hero, 36px section headings, 16–18px body). Ten actual client logos are recorded in content/client-logos.json. The reference layout is adapted with a logo strip, independent project-highlight and process carousels, hand icon, white platform labels and responsive spacing. Carousel text is agency project/process copy, not a customer testimonial.

## Motion and mobile repair

The permanent hand icon is removed. The reference gesture JSON (https://paulnrogers.com/wp-content/uploads/2022/06/lf30_editor_t9bloiua.json, 94 frames at 60fps) plays once below the process carousel dots on viewport entry. Lottie Web 5.12.2 light SVG player is loaded lazily, with its MIT license retained. Desktop client logos move horizontally with scroll; mobile uses the reference’s static grid behavior. Carousels transition at 500ms and advance every 5s while visible, pausing on hover, interaction, document hiding and reduced motion. Touch swipe and keyboard arrows are supported. Slide height is stable. Guide covers have consistent white text; phone cards stack. Browser checks cover 320/390px layouts, mobile menu and search, gesture completion and stable carousel height. Physical phones were not tested.
