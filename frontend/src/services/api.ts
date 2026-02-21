import axios from "axios";
import { API_BASE_URL, STORAGE_KEYS } from "../constants";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use(async (config) => {
  // TODO: AsyncStorage에서 토큰 가져오기
  // const token = await AsyncStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN);
  // if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    // TODO: 401 시 토큰 갱신 로직
    return Promise.reject(error);
  }
);

export default api;
