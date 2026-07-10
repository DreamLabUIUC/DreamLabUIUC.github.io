import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://dream.ischool.illinois.edu',
  base: '/secfid',
  trailingSlash: 'always',
  compressHTML: true,
});
