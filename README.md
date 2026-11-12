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

This is a review version, not a verified pixel-perfect copy. It follows the supplied reference's black/white/blush section structure, Jost typography, outlined buttons, project grid, quote bubble and guide cards. Copy and branding are adapted to Fazal. The signature is a temporary text wordmark. Project covers are authored illustrative graphics; replace them with approved real screenshots. The client quote slots are explicitly labelled placeholders and must be replaced or removed before public launch. Contact links point to Xylo Solutions; no contact form or newsletter service is configured. Guides are initial editorial drafts, not researched traffic guarantees.

The static site has no admin panel or server-side backend. Content is edited in GitHub/the source files. Search runs in the visitor's browser. Fonts currently load from Google Fonts' font CDN, using `font-display: swap`; no analytics or tracking scripts are included.

## SEO

Each page includes a title, description, canonical URL and basic Open Graph metadata. A sitemap and robots.txt target https://fazalbinmahmood.com. Use a preview deployment for review; finish content before connecting the production domain. Search rankings are not guaranteed.

## Validation

JavaScript syntax and local internal link/asset integrity are checked. Browser QA covers desktop rendering, local search, carousel selection, and mobile/tablet iframe layouts. This does not substitute for testing on physical iOS and Android devices.
