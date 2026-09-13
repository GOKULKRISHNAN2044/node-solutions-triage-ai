import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
  headers: { "Content-Type": "application/json" },
});

export const triageRequest = async (requestText) => {
  const res = await api.post("/api/triage", { request_text: requestText });
  return res.data;
};

export const getHistory = async () => {
  const res = await api.get("/api/history");
  return res.data;
};

export default api;
