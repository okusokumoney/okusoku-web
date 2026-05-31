import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

import cloudflare from "@astrojs/cloudflare";

export default defineConfig({
  site: 'https://okusoku.com',
  trailingSlash: 'always',
  integrations: [sitemap()],
  output: "hybrid",
  adapter: cloudflare()
});