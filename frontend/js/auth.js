const AUTH = {
    API_URL: (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
        ? 'http://127.0.0.1:8000/api'
        : window.location.origin + '/api',

    getToken() {
        return localStorage.getItem('token');
    },

    getUser() {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    },

    isAuthenticated() {
        const token = this.getToken();
        if (!token) return false;
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            return payload.exp * 1000 > Date.now();
        } catch {
            return false;
        }
    },

    getHeaders() {
        const headers = { 'Content-Type': 'application/json' };
        const token = this.getToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        return headers;
    },

    escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    },

    async apiGet(endpoint) {
        const response = await fetch(`${this.API_URL}${endpoint}`, {
            headers: this.getHeaders()
        });
        if (!response.ok) {
            if (response.status === 401) {
                this.logout();
                window.location.href = 'login.html';
            }
            throw new Error(`HTTP ${response.status}`);
        }
        return response.json();
    },

    async apiPost(endpoint, data) {
        const response = await fetch(`${this.API_URL}${endpoint}`, {
            method: 'POST',
            headers: this.getHeaders(),
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            if (response.status === 401) {
                this.logout();
                window.location.href = 'login.html';
            }
            const error = await response.json().catch(() => ({}));
            throw new Error(error.detail || error.message || `HTTP ${response.status}`);
        }
        return response.json();
    },

    logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
    },

    requireAuth() {
        if (!this.isAuthenticated()) {
            window.location.href = 'login.html';
        }
    },

    updateNavbar() {
        const user = this.getUser();
        const navUser = document.getElementById('nav-user');
        if (navUser) {
            if (user) {
                const email = this.escapeHtml(user.email || user.username || '');
                navUser.innerHTML = `
                    <span class="navbar-text">
                        <i class="bi bi-person-circle me-1"></i>${email}
                    </span>
                    <button class="btn btn-sm btn-outline-light ms-2" onclick="AUTH.logout()">
                        <i class="bi bi-box-arrow-right me-1"></i>Salir
                    </button>
                `;
            } else {
                navUser.innerHTML = `
                    <a href="login.html" class="btn btn-sm btn-outline-light">
                        <i class="bi bi-box-arrow-in-right me-1"></i>Iniciar Sesion
                    </a>
                `;
            }
        }
    }
};
