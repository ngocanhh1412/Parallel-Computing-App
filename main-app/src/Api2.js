import axios from "axios";

const API_URL = "http://localhost:8001"; // Đặt URL của API FastAPI của bạn ở đây

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export async function callAddAPI2(inputString, inputOption) {
  try {
    const response = await api.post("/fcmParallel", { input_string: inputString, input_option: inputOption});
    return response.data.result;
  } catch (error) {
    console.error("API Error:", error);
    throw new Error("Failed to call add API");
  }
}