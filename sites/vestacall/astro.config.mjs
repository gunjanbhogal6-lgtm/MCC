import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import compress from 'astro-compress';
import robotsTxt from 'astro-robots-txt';

function customSitemap() {
  return {
    name: 'custom-sitemap',
    hooks: {
      'astro:build:done': async ({ dir, pages }) => {
        const fs = await import('node:fs/promises');
        const siteUrl = 'https://vestacall.com';

        let xml = '<?xml version="1.0" encoding="UTF-8"?>\n';
        xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';

        for (const page of pages) {
          if (page.pathname === '404/' || page.pathname === '404') continue;

          let loc = siteUrl;
          if (page.pathname) {
            loc += '/' + page.pathname;
          }

          xml += `  <url>\n    <loc>${loc}</loc>\n  </url>\n`;
        }

        xml += '</urlset>';

        await fs.writeFile(new URL('sitemap-index.xml', dir), xml);
        await fs.writeFile(new URL('sitemap-0.xml', dir), xml);
        console.log('✅ Custom sitemap generated successfully.');
      }
    }
  };
}

export default defineConfig({
  site: 'https://vestacall.com',
  output: 'static',
  integrations: [
    tailwind(),
    customSitemap(),
    robotsTxt({
      policy: [
        {
          userAgent: '*',
          allow: '/',
        }
      ],
      sitemap: false, // We'll rely on the generated files locally
    }),
    compress({
      CSS: true,
      HTML: true,
      JavaScript: true,
      Image: true,
    }),
  ],
  build: {
    inlineStylesheets: 'auto',
  },
});