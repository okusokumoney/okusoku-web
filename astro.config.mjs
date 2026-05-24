import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://reliable-pixie-d80d76.netlify.app',
  trailingSlash: 'always',
  integrations: [sitemap()],
});
