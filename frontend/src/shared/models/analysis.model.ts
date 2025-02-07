import { z } from "zod";

// ! 👇 Zod Schema
export const StatisticsSchema = z.object({
	mean: z.number(),
	median: z.number(),
	std: z.number(),
});

export const AnalysisStatsSchema = z.object({
	price_stats: StatisticsSchema,
	quantity_stats: StatisticsSchema,
	rating_stats: StatisticsSchema,
});

export const AnomalyTypeEnum = z.enum(["PRICE", "QUANTITY", "RATING"]);
export const AnomalySeverityEnum = z.enum(["LOW", "MEDIUM", "HIGH"]);
export const AnalysisStatusEnum = z.enum([
	"PENDING",
	"PROCESSING",
	"COMPLETED",
	"FAILED",
]);

export const AnomalySchema = z.object({
	product_id: z.number(),
	type: AnomalyTypeEnum,
	value: z.number(),
	expected_range: z.tuple([z.number(), z.number()]),
	severity: AnomalySeverityEnum,
	message: z.string(),
});

export const AnalysisSchema = z.object({
	fileId: z.string(),
	status: AnalysisStatusEnum,
	statistics: AnalysisStatsSchema,
	anomalies: z.array(AnomalySchema),
	metadata: z.object({
		filename: z.string(),
		processing_time: z.number(),
		valid_records: z.object({
			price: z.number(),
			quantity: z.number(),
			rating: z.number(),
		}),
	}),
	total_rows: z.number(),
	anomaly_count: z.number(),
});

// ! 👇 API Response schemas
export const GetAnalysesResponseSchema = z.object({
	items: z.array(AnalysisSchema),
	count: z.number(),
});

export const GetAnalysisResponseSchema = AnalysisSchema;

// ! 👇 Types
export type Statistics = z.infer<typeof StatisticsSchema>;
export type AnalysisStats = z.infer<typeof AnalysisStatsSchema>;
export type AnomalyType = z.infer<typeof AnomalyTypeEnum>;
export type AnomalySeverity = z.infer<typeof AnomalySeverityEnum>;
export type AnalysisStatus = z.infer<typeof AnalysisStatusEnum>;
export type Anomaly = z.infer<typeof AnomalySchema>;
export type Analysis = z.infer<typeof AnalysisSchema>;
export type GetAnalysesResponse = z.infer<typeof GetAnalysesResponseSchema>;
export type GetAnalysisResponse = z.infer<typeof GetAnalysisResponseSchema>;
