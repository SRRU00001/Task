// API Client for backend communication
// Uses CONFIG.API_BASE_URL from config.js, falls back to '/api' for local dev
const API_BASE_URL = (window.CONFIG && window.CONFIG.API_BASE_URL) || '/api';

class API {
    constructor() {
        this.token = localStorage.getItem('admin_token');
    }

    setToken(token) {
        this.token = token;
        if (token) {
            localStorage.setItem('admin_token', token);
        } else {
            localStorage.removeItem('admin_token');
        }
    }

    getAuthHeader() {
        if (this.token) {
            return { 'Authorization': `Bearer ${this.token}` };
        }
        return {};
    }

    async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const isFormData = options.body instanceof FormData;
        
        // Build headers
        const headers = {};
        
        // Add Content-Type only for JSON requests (not FormData)
        if (!isFormData && options.method && options.method !== 'GET') {
            headers['Content-Type'] = 'application/json';
        }
        
        // Add auth header if required
        if (options.requireAuth) {
            Object.assign(headers, this.getAuthHeader());
        }
        
        // Merge with custom headers (but don't override FormData behavior)
        if (options.headers && !isFormData) {
            Object.assign(headers, options.headers);
        } else if (options.headers && isFormData) {
            // For FormData, only add auth header from custom headers
            if (options.headers['Authorization']) {
                headers['Authorization'] = options.headers['Authorization'];
            }
        }

        const config = {
            method: options.method || 'GET',
            headers: headers,
        };
        
        if (options.body) {
            config.body = options.body;
        }

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Request failed');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Public endpoints
    async getProjects() {
        return this.request('/projects');
    }

    async getClients() {
        return this.request('/clients');
    }

    async submitContact(formData) {
        return this.request('/contact', {
            method: 'POST',
            body: JSON.stringify(formData),
        });
    }

    async subscribeNewsletter(email) {
        return this.request('/newsletter', {
            method: 'POST',
            body: JSON.stringify({ email }),
        });
    }

    // Admin endpoints
    async login(username, password) {
        return this.request('/admin/auth/login', {
            method: 'POST',
            body: JSON.stringify({ username, password }),
        });
    }

    async verifyAdmin() {
        return this.request('/admin/auth/verify', {
            requireAuth: true,
        });
    }

    // Admin - Projects (uses FormData for file upload)
    async createProject(formData) {
        const url = `${API_BASE_URL}/admin/projects`;
        const response = await fetch(url, {
            method: 'POST',
            headers: this.getAuthHeader(),
            body: formData,
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || 'Request failed');
        }
        return data;
    }

    async updateProject(id, formData) {
        const url = `${API_BASE_URL}/admin/projects/${id}`;
        const response = await fetch(url, {
            method: 'PUT',
            headers: this.getAuthHeader(),
            body: formData,
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || 'Request failed');
        }
        return data;
    }

    async deleteProject(id) {
        return this.request(`/admin/projects/${id}`, {
            method: 'DELETE',
            requireAuth: true,
        });
    }

    // Admin - Clients (uses FormData for file upload)
    async createClient(formData) {
        const url = `${API_BASE_URL}/admin/clients`;
        const response = await fetch(url, {
            method: 'POST',
            headers: this.getAuthHeader(),
            body: formData,
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || 'Request failed');
        }
        return data;
    }

    async updateClient(id, formData) {
        const url = `${API_BASE_URL}/admin/clients/${id}`;
        const response = await fetch(url, {
            method: 'PUT',
            headers: this.getAuthHeader(),
            body: formData,
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || 'Request failed');
        }
        return data;
    }

    async deleteClient(id) {
        return this.request(`/admin/clients/${id}`, {
            method: 'DELETE',
            requireAuth: true,
        });
    }

    // Admin - Contacts
    async getContacts() {
        return this.request('/admin/contacts', {
            requireAuth: true,
        });
    }

    // Admin - Newsletters
    async getNewsletters() {
        return this.request('/admin/newsletters', {
            requireAuth: true,
        });
    }
}

const api = new API();

