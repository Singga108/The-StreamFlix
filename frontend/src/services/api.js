import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API_BASE = `${BACKEND_URL}/api`;

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user');
      // Optionally redirect to login
    }
    return Promise.reject(error);
  }
);

// Auth APIs
export const authAPI = {
  register: (userData) => api.post('/auth/register', userData),
  login: (credentials) => api.post('/auth/login', credentials),
  getProfile: () => api.get('/user/profile'),
};

// Movies APIs
export const moviesAPI = {
  getTrending: (page = 1) => api.get(`/movies/trending?page=${page}`),
  getPopular: (page = 1) => api.get(`/movies/popular?page=${page}`),
  getDetails: (movieId) => api.get(`/movies/${movieId}`),
};

// Series APIs
export const seriesAPI = {
  getTrending: (page = 1) => api.get(`/series/trending?page=${page}`),
  getDetails: (seriesId) => api.get(`/series/${seriesId}`),
};

// Sports APIs
export const sportsAPI = {
  getLive: () => api.get('/sports/live'),
  getHighlights: () => api.get('/sports/highlights'),
  getUpcoming: () => api.get('/sports/upcoming'),
  getAll: () => api.get('/sports/all'),
};

// Search API
export const searchAPI = {
  searchContent: (query, page = 1) => api.get(`/search?q=${encodeURIComponent(query)}&page=${page}`),
};

// Watchlist APIs
export const watchlistAPI = {
  add: (contentData) => api.post('/user/watchlist', contentData),
  get: () => api.get('/user/watchlist'),
  remove: (contentId) => api.delete(`/user/watchlist/${contentId}`),
};

export default api;