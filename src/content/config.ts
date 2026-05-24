import { defineCollection, z } from 'astro:content';

const articles = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    pubDate: z.string(),
    category: z.string(),
    tags: z.array(z.string()).optional(),
    affiliate: z.array(z.object({
      label: z.string(),
      url: z.string(),
      description: z.string().optional(),
    })).optional(),
  }),
});

export const collections = { articles };
