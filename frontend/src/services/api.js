import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
  headers: { "Content-Type": "application/json" },
});

export const loginUser = async (username, password) => {
  const res = await api.post("/api/auth/login", { username, password });
  return res.data;
};

export const triageRequest = async (requestText) => {
  const res = await api.post("/api/triage", { request_text: requestText });
  return res.data;
};

export const getHistory = async () => {
  const res = await api.get("/api/history");
  return res.data;
};

export default api;
