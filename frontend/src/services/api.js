import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true,
});

export const vendorService = {
    async getAllVendors() {
        const response = await api.get('/vendors/');
        return response.data;
    },

    async getVendor(id) {
        const response = await api.get(`/vendors/${id}/`);
        return response.data;
    },

    async trackClick(vendorId) {
        const response = await api.post(`/vendors/${vendorId}/track_click/`);
        return response.data;
    },
};

export const modelService = {
    async getAllModels(vendorId = null) {
        const params = vendorId ? { vendor: vendorId } : {};
        const response = await api.get('/models/', { params });
        return response.data;
    },

    async getModel(id) {
        const response = await api.get(`/models/${id}/`);
        return response.data;
    },
};

export const consultationService = {
    async submitRequest(data) {
        const response = await api.post('/consultations/', data);
        return response.data;
    },
};

export default api;
