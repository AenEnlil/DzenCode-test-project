import axios from 'axios';
import { getAccessToken, refreshToken } from '@/services/authService.js';

const api = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_API_URL,
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('access');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            const refresh = localStorage.getItem('refresh')
            try {
                if (refresh) {
                    // get new access token if refresh exists
                    const tokens = await refreshToken(refresh)
                    localStorage.setItem('access', tokens.access)
                    originalRequest.headers['Authorization'] = `Bearer ${tokens.access}`
                    return api(originalRequest)
                } else {
                    // get new token pair
                    const tokens = await getAccessToken()
                    localStorage.setItem('access', tokens.access)
                    localStorage.setItem('refresh', tokens.refresh)
                    originalRequest.headers['Authorization'] = `Bearer ${tokens.access}`
                    return api(originalRequest)
                }
            } catch (err) {
                console.log('Auth failed', err)
                // if failed to get new token(refresh expired) try to get new token pair
                try {
                    const tokens = await getAccessToken(); // создаёт нового "гостя"
                    localStorage.setItem('access', tokens.access);
                    localStorage.setItem('refresh', tokens.refresh);
                    originalRequest.headers['Authorization'] = `Bearer ${tokens.access}`;
                    return api(originalRequest);  // повторяем исходный запрос
                } catch (e) {
                     console.error('Access token creation failed', e);
                     localStorage.removeItem('access');
                     localStorage.removeItem('refresh');
                     return Promise.reject(error);  // финальный отказ
                }
            }
        }
        return Promise.reject(error)
    }
)

export default api;