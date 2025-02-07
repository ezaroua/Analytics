import axios from "axios";
import { apiV1 } from "../core/axios-instance";
import type {
	GetAnalysesResponse,
	GetAnalysisResponse,
} from "../models/analysis.model";

export const AnalysisApi = {
	getAnalyses: async (): Promise<GetAnalysesResponse> => {
		const response = await apiV1.get<GetAnalysesResponse>("/analyses");
		return response.data;
		// return GetAnalysesResponseSchema.parse(response.data);
	},

	getAnalysis: async (fileId: string): Promise<GetAnalysisResponse> => {
		const response = await apiV1.get<GetAnalysisResponse>(
			`/analyses/${fileId}`,
		);
		// return GetAnalysisResponseSchema.parse(response.data);
		return response.data;
	},

	getUploadUrl: async (
		fileName: string,
	): Promise<{ uploadUrl: string; fileId: string }> => {
		const response = await apiV1.post("/upload", { fileName });
		return response.data;
	},

	// * Upload file using presigned URL with progress tracking
	uploadFile: async (
		url: string,
		file: File,
		onProgress?: (progressEvent: number) => void,
	): Promise<void> => {
		await axios.put(url, file, {
			headers: {
				"Content-Type": "text/csv",
			},
			onUploadProgress: (progressEvent) => {
				if (progressEvent.total) {
					const percentCompleted =
						(progressEvent.loaded * 100) / progressEvent.total;
					onProgress?.(percentCompleted);
				}
			},
		});
	},
};
