import axios from 'axios';

const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
    timeout: 15000,
    headers: {
        'Content-Type': 'application/json',
    },
});

export async function suggestText(payload) {
    const response = await apiClient.post('/suggest', payload);
    return response.data;
}

export async function rewriteText(payload) {
    const response = await apiClient.post('/rewrite', payload);
    return response.data;
}