import axios from "axios";

const API_URL = "http://localhost:8000"; // Đặt URL của API FastAPI của bạn ở đây

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export async function callAddAPI(inputString) {
  try {
    const response = await api.post("/fcm", { input_string: inputString });
    return response.data.result;
  } catch (error) {
    console.error("API Error:", error);
    throw new Error("Failed to call add API");
  }
}