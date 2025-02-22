import axios from "axios";
import { apiV1 } from "../core/axios-instance";
import type { Analysis } from "../models/analysis.model";

export const AnalysisApi = {
	getAnalyses: async (): Promise<Analysis[]> => {
		const response = await apiV1.get("/analyses");
		return response.data;
	},

	getAnalysis: async (fileId: string): Promise<Analysis> => {
		const response = await apiV1.get(`/analyses/${fileId}`);
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
