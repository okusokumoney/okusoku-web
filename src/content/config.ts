import { defineCollection, z } from 'astro:content';

const articles = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    pubDate: z.string(),
    category: z.string(),
    image: z.string().optional(),
    type: z.enum(['article', 'news', 'book', 'note']).optional(),
    sourceUrl: z.string().optional(),
    sourceName: z.string().optional(),
    tags: z.array(z.string()).optional(),
    affiliate: z.array(z.object({
      label: z.string(),
      url: z.string(),
      description: z.string().optional(),
    })).optional(),
  }),
});

export const collections = { articles };
