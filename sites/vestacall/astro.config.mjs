import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import compress from 'astro-compress';
import robotsTxt from 'astro-robots-txt';

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
  ],
  build: {
    inlineStylesheets: 'always',
  },
});