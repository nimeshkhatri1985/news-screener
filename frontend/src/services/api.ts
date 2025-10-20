import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
}) as AxiosInstance & {
  getSources: typeof getSources;
  createSource: typeof createSource;
  getArticles: typeof getArticles;
  searchArticles: typeof searchArticles;
  getFilters: typeof getFilters;
  createFilter: typeof createFilter;
  getPosts: typeof getPosts;
  createPost: typeof createPost;
};

// Types
export interface Source {
  id: number;
  name: string;
  url: string;
  rss_feed: string;
  is_active: boolean;
  created_at: string;
}

export interface Article {
  id: number;
  source_id: number;
  title: string;
  content: string;
  url: string;
  published_at: string;
  crawled_at: string;
}

export interface Filter {
  id: number;
  name: string;
  keywords: string;
  is_active: boolean;
  created_at: string;
}

export interface Post {
  id: number;
  article_id: number;
  content: string;
  posted_at: string | null;
  twitter_id: string | null;
  status: string;
}

// API Methods
export const getSources = async (): Promise<Source[]> => {
  const response = await api.get('/sources');
  return response.data;
};

export const createSource = async (source: Omit<Source, 'id' | 'created_at'>): Promise<Source> => {
  const response = await api.post('/sources', source);
  return response.data;
};

export const getArticles = async (params?: {
  source_id?: number;
  keywords?: string;
  category?: string;
  date_from?: string;
  date_to?: string;
  limit?: number;
  offset?: number;
}): Promise<Article[]> => {
  const response = await api.get('/articles', { params });
  return response.data;
};

export const searchArticles = async (params: {
  q: string;
  source_id?: number;
  limit?: number;
  offset?: number;
}): Promise<Article[]> => {
  const response = await api.get('/search', { params });
  return response.data;
};

export const getFilters = async (): Promise<Filter[]> => {
  const response = await api.get('/filters');
  return response.data;
};

export const createFilter = async (filter: Omit<Filter, 'id' | 'created_at'>): Promise<Filter> => {
  const response = await api.post('/filters', filter);
  return response.data;
};

export const getPosts = async (): Promise<Post[]> => {
  const response = await api.get('/posts');
  return response.data;
};

export const createPost = async (post: Omit<Post, 'id' | 'posted_at' | 'twitter_id' | 'status'>): Promise<Post> => {
  const response = await api.post('/posts', post);
  return response.data;
};

// Export API functions as methods on the api object
api.getSources = getSources;
api.createSource = createSource;
api.getArticles = getArticles;
api.searchArticles = searchArticles;
api.getFilters = getFilters;
api.createFilter = createFilter;
api.getPosts = getPosts;
api.createPost = createPost;

export default api;
