import { z } from "zod";

// * Basic schemas
export const ProductSchema = z.object({
	id: z.string(),
	name: z.string(),
	price: z.number().min(10).max(500),
	quantity: z.number().min(1).max(50),
	customerRating: z.number().min(1).max(5),
});

export const StatisticsSchema = z.object({
	mean: z.number(),
	median: z.number(),
	std: z.number(),
});

// * Input schemas
export const FileUploadSchema = z.object({
	filename: z.string(),
	contentType: z.literal("text/csv"),
	size: z.number(),
});

export const AnalysisRequestSchema = z.object({
	fileId: z.string(),
	timestamp: z.string(),
	data: z.array(ProductSchema),
});

// * Output schemas
export const AnomalySchema = z.object({
	productId: z.string(),
	type: z.enum(["price", "quantity", "rating"]),
	value: z.number(),
	expectedRange: z.tuple([z.number(), z.number()]),
	severity: z.enum(["low", "medium", "high"]),
	message: z.string(),
});

export const StatisticalAnalysisSchema = z.object({
	price_stats: StatisticsSchema,
	quantity_stats: StatisticsSchema,
	rating_stats: StatisticsSchema,
});

export const AnomalyAnalysisSchema = z.object({
	price_anomalies: z.array(z.string()),
	quantity_anomalies: z.array(z.string()),
	rating_anomalies: z.array(z.string()),
});

export const AnalysisResultSchema = z.object({
	fileId: z.string(),
	filename: z.string(),
	timestamp: z.string(),
	status: z.enum(["processing", "completed", "failed"]),
	results: z.object({
		statistics: StatisticalAnalysisSchema,
		anomalies: AnomalyAnalysisSchema,
		details: z.array(AnomalySchema),
	}),
	metadata: z.object({
		processingTime: z.number(),
		rowCount: z.number(),
		anomalyCount: z.number(),
	}),
});

// * DynamoDB schemas
export const DynamoAnalysisSchema = z.object({
	fileId: z.string(),
	timestamp: z.string(),
	filename: z.string(),
	status: z.enum(["processing", "completed", "failed"]),
	results: z.string(), // * JSON stringified AnalysisResult
	metadata: z.object({
		processingTime: z.number(),
		rowCount: z.number(),
		anomalyCount: z.number(),
	}),
});

export const DynamoFileSchema = z.object({
	fileId: z.string(),
	timestamp: z.string(),
	filename: z.string(),
	size: z.number(),
	status: z.enum(["uploaded", "processing", "analyzed", "failed"]),
	s3Key: z.string(),
});

// * Types
export type Product = z.infer<typeof ProductSchema>;
export type FileUpload = z.infer<typeof FileUploadSchema>;
export type AnalysisRequest = z.infer<typeof AnalysisRequestSchema>;
export type AnalysisResult = z.infer<typeof AnalysisResultSchema>;
export type Anomaly = z.infer<typeof AnomalySchema>;
export type DynamoAnalysis = z.infer<typeof DynamoAnalysisSchema>;
export type DynamoFile = z.infer<typeof DynamoFileSchema>;
