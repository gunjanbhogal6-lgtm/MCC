// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

// Phase 1: Core SEO Integrations
import sitemap from '@astrojs/sitemap';
import robotsTxt from 'astro-robots-txt';

// Note: astro-canonical and astro-capo had compatibility issues with Astro 5.x
// Manual head ordering and canonical validation implemented in Layout.astro

// https://astro.build/config
export default defineConfig({
  site: 'https://salamtalk.com', // Required for sitemap, canonicals, SEO

  vite: {
    plugins: [tailwindcss()]
  },

  integrations: [
    // Phase 1: Core SEO
    sitemap({
      changefreq: 'weekly',
      priority: 0.7,
      lastmod: new Date(),
    }),

    robotsTxt({
      policy: [
        {
          userAgent: '*',
          allow: '/',
          disallow: ['/api/', '/admin/'],
        },
      ],
    }),

    // Note: Manual implementation for advanced features:
    // - Schema markup: in Layout.astro (astro-seo-schema compatible)
    // - Canonical validation: in Layout.astro
    // - Head element ordering: in Layout.astro
  ],
});