import api from "./api";

export const authService = {
  login: (email: string, password: string) =>
    api.post("/api/auth/login", { email, password }),

  register: (email: string, password: string, name: string) =>
    api.post("/api/auth/register", { email, password, name }),

  refresh: (refreshToken: string) =>
    api.post("/api/auth/refresh", { refresh_token: refreshToken }),
};
