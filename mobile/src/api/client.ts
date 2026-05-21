/**
 * UstaadJi API Client
 * Handles communication with the FastAPI backend.
 */
import { Platform } from 'react-native';

// Android emulator uses 10.0.2.2, iOS sim & web use localhost
const getBaseUrl = (): string => {
  if (Platform.OS === 'android') return 'http://10.0.2.2:8000';
  return 'http://localhost:8000';
};

const BASE_URL = getBaseUrl();

// ── Types ────────────────────────────────────────────────────────────────

export interface ChatRequest {
  message: string;
  user_id: string;
  session_id: string | null;
}

export interface ChatResponse {
  response: string;
  session_id: string;
  user_id: string;
}

export interface BookingRequest {
  provider_id: number;
  user_id: string;
  service_description?: string;
  session_id?: string;
}

export interface BookingResponse {
  booking_id: string;
  status: string;
  provider_name: string;
  provider_phone: string | null;
  provider_category: string;
  message: string;
  estimated_arrival: string;
  booked_at: string;
}

export interface HealthResponse {
  status: string;
  gemini_key_configured: boolean;
  maps_key_configured: boolean;
  model: string;
  pipeline: string;
  endpoints: string[];
}

// ── API Calls ────────────────────────────────────────────────────────────

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const url = `${BASE_URL}${path}`;
  console.log(`[API] ${options?.method ?? 'GET'} ${url}`);

  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });

  if (!res.ok) {
    const body = await res.text();
    throw new Error(`API error ${res.status}: ${body}`);
  }

  return res.json() as Promise<T>;
}

/** Send a chat message through the 5-agent pipeline. */
export async function sendMessage(req: ChatRequest): Promise<ChatResponse> {
  return request<ChatResponse>('/api/chat', {
    method: 'POST',
    body: JSON.stringify(req),
  });
}

/** Create a booking for a provider. */
export async function createBooking(req: BookingRequest): Promise<BookingResponse> {
  return request<BookingResponse>('/api/booking', {
    method: 'POST',
    body: JSON.stringify(req),
  });
}

/** Check backend health. */
export async function checkHealth(): Promise<HealthResponse> {
  return request<HealthResponse>('/api/health');
}
