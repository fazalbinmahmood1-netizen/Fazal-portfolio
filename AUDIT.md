# Portfolio audit — 14 November 2026

Checked all 81 content pages plus the 404 document for internal link targets, image targets, heading presence and alt attributes: 3,100 references, no missing local targets. Browser responsive harness checked all 81 content pages at 320, 390, 768 and 1440 px: 324 checks, no page-level horizontal overflow. This is a layout metric, not a pixel-perfect comparison of every page.

Live browser verified homepage, service search and destination, contact navigation, blog listing/search. Local browser verified mobile menu open/close and carousel dot navigation. Paul Rogers homepage was opened for structural comparison; branding and content remain Xylo's.

Changes: parallel font stylesheet discovery and font-host preconnect; preserve query parameters on trailing-slash redirects; branded HTTP 404 for missing pages; reject nonexistent blog pagination; canonical redirect page 1; pause carousel while focus is within it; respect CMS article URLs in blog search; omit duplicate pagination entries from global search.

Validation: CMS authorization, owner binding, CSRF, input validation, stale writes, draft/publish separation, restore and export regression tests pass. Added public routing regression tests pass. CSS/font change removes a serial stylesheet import; existing lazy-loaded WebP imagery and deferred JS retained.

Limits: no Lighthouse or real-user Core Web Vitals score obtained. HTTP crawler access from the executor returned 403 while the live browser worked, so generated-page validation is not a successful live HTTP crawl. Authenticated admin editing, real email delivery, every external destination and physical iOS/Android hardware were not verified. Contact uses email and the agency contact page; there is no newsletter subscription backend. Do not describe the site as 100% identical or universally tested.
