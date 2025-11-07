import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API methods
export const apiClient = {
  // Convert image to DXF
  convertImage: async (file, threshold) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('threshold', threshold);

    const response = await api.post('/api/convert', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Get conversion history
  getHistory: async (search = '', page = 1, limit = 20) => {
    const response = await api.get('/api/history', {
      params: { search, page, limit },
    });
    return response.data;
  },

  // Download DXF file
  downloadDXF: async (conversionId) => {
    const response = await api.get(`/api/download/${conversionId}`, {
      responseType: 'blob',
    });
    return response.data;
  },

  // Get thumbnail
  getThumbnailUrl: (conversionId) => {
    return `${API_BASE_URL}/api/thumbnail/${conversionId}`;
  },

  // Delete conversion
  deleteConversion: async (conversionId) => {
    const response = await api.delete(`/api/delete/${conversionId}`);
    return response.data;
  },

  // Get stats
  getStats: async () => {
    const response = await api.get('/api/stats');
    return response.data;
  },
};

export default apiClient;
