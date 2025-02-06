import axios, { HttpStatusCode, type AxiosError } from "axios";

const BASE_URL = import.meta.env.VITE_API_URL;

console.log("BASE_URL", BASE_URL);

export const apiV1 = axios.create({
	baseURL: BASE_URL,
	timeout: 10000,
	headers: {
		"Content-Type": "application/json",
	},
});

// * Request interceptor
// axiosInstance.interceptors.request.use(
// 	(config) => {
// 		const token = localStorage.getItem("token");
// 		if (token) {
// 			config.headers.Authorization = `Token ${token}`;
// 		}
// 		return config;
// 	},
// 	(error) => Promise.reject(error),
// );

// * Response interceptor
apiV1.interceptors.response.use(
	(response) => {
		return response;
	},
	(error: AxiosError) => {
		if (error.response?.status === HttpStatusCode.Unauthorized) {
			localStorage.removeItem("token");
		}
		return Promise.reject(error);
	},
);
