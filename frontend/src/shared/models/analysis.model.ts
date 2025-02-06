import { z } from "zod";

// ! 👇 Zod Schema
export const AnalysisSchema = z.object({
	fileId: z.string(),
	timestamp: z.string(),
	results: z.object({
		statistics: z.object({
			price_stats: z.object({
				mean: z.number(),
				median: z.number(),
				std: z.number(),
			}),
			quantity_stats: z.object({
				mean: z.number(),
				median: z.number(),
				std: z.number(),
			}),
			rating_stats: z.object({
				mean: z.number(),
				median: z.number(),
				std: z.number(),
			}),
		}),
		anomalies: z.object({
			price_anomalies: z.array(z.string()),
			quantity_anomalies: z.array(z.string()),
			rating_anomalies: z.array(z.string()),
		}),
	}),
});

// ! 👇 Types
export type Analysis = z.infer<typeof AnalysisSchema>;
