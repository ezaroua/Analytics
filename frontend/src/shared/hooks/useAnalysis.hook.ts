import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { AnalysisApi } from "../api/analysis-api";

export const analysisQueryKeys = {
	all: ["analyses"],
	one: (fileId: string) => ["analysis", fileId],
};

export const useAnalyses = () => {
	return useQuery({
		queryKey: analysisQueryKeys.all,
		queryFn: AnalysisApi.getAnalyses,
	});
};

export const useAnalysis = (fileId: string) => {
	return useQuery({
		enabled: !!fileId,
		queryKey: analysisQueryKeys.one(fileId),
		queryFn: () => AnalysisApi.getAnalysis(fileId),
	});
};

export const useFileUpload = () => {
	const queryClient = useQueryClient();

	return useMutation({
		mutationFn: async ({
			file,
			onProgress,
		}: {
			file: File;
			onProgress?: (progress: number) => void;
		}) => {
			const { uploadUrl, fileId } = await AnalysisApi.getUploadUrl(file.name);
			await AnalysisApi.uploadFile(uploadUrl, file, onProgress);
			return { fileId };
		},
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: analysisQueryKeys.all });
		},
	});
};
