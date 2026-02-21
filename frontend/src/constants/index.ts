export const API_BASE_URL = __DEV__
  ? "http://localhost:8000"
  : "https://api.example.com";

export const COLORS = {
  primary: "#4A90D9",
  secondary: "#7B61FF",
  background: "#FFFFFF",
  text: "#1A1A1A",
  textSecondary: "#6B7280",
  border: "#E5E7EB",
  error: "#EF4444",
  success: "#10B981",
} as const;

export const STORAGE_KEYS = {
  ACCESS_TOKEN: "access_token",
  REFRESH_TOKEN: "refresh_token",
} as const;
