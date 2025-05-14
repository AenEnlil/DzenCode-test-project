import axios from 'axios';
import {API_BASE_URL} from '@/config.js'

export async function getAccessToken() {
  const response = await axios.post(`${API_BASE_URL}/tokens/create/`);
  return response.data;
}

export async function refreshToken(refresh) {
  const response = await axios.post(`${API_BASE_URL}/tokens/refresh/`, { refresh });
  return response.data;
}