# Site Manager

Custom editor at /admin/ and manage.fazalbinmahmood.com. Visitors remain anonymous; administration uses Sites' verified ChatGPT identity restricted to the configured ADMIN_EMAIL and pinned owner ID. This deployment depends on Sites hosting, authentication and R2 storage. No paid AI API is called by the CMS.

Edit page content, blog posts, projects, images and typography/colours. Save draft, preview, then publish. Publishing preserves up to ten previous documents. Restore sends a version to draft; publish separately. Export downloads content/settings JSON; uploaded image files must be backed up separately. Content edits are stored in R2, not automatically committed to GitHub. Source is maintained in Git.

Build: python scripts/build.py; python scripts/blog.py; python scripts/build-cms.py. Requires Python lxml. Test: node scripts/test-cms.mjs. Worker entrypoint: dist/server/index.js. Hosting must bind R2 as BUCKET and set ADMIN_EMAIL as a server secret. Never embed credentials in client code.

Existing main-page text, links and images are editable. New blog and project pages support paragraphs and ## headings. Header/footer structure and arbitrary new layout sections still require code changes. This is a structured content editor, not a drag-and-drop page builder.
