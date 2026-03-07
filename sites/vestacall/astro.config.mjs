import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import compress from 'astro-compress';
import robotsTxt from 'astro-robots-txt';

import react from '@astrojs/react';

export default defineConfig({
  site: 'https://vestacall.com',
  output: 'static',

  integrations: [
    tailwind(),
    robotsTxt({
      policy: [
        {
          userAgent: '*',
          allow: '/',
        }
      ],
      sitemap: 'https://vestacall.com/sitemap.xml',
    }),
    compress({
      CSS: true,
      HTML: true,
      JavaScript: true,
      Image: true,
    }),
    {
      name: 'sitemap-generator',
      hooks: {
        'astro:build:done': async ({ dir, pages }) => {
          const fs = await import('node:fs/promises');
          const siteUrl = 'https://vestacall.com';

          let xml = '<?xml version="1.0" encoding="UTF-8"?>\n';
          xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';

          for (const page of pages) {
            // Exclude 404 page
            if (page.pathname.includes('404')) continue;

            const loc = new URL(page.pathname, siteUrl).href.replace(/\/$/, '') + '/';
            xml += `  <url>\n    <loc>${loc}</loc>\n  </url>\n`;
          }

          xml += '</urlset>';

          await fs.writeFile(new URL('sitemap.xml', dir), xml);
          console.log('✅ sitemap.xml generated successfully.');
        }
      }
    }
  ],

  build: {
    inlineStylesheets: 'always',
  },
});