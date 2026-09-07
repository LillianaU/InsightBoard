const AUTH = {
    API_URL: 'http://127.0.0.1:8000/api',

    getToken() {
        return localStorage.getItem('token');
    },

    getUser() {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    },

    isAuthenticated() {
        return !!this.getToken();
    },

    getHeaders() {
        const headers = { 'Content-Type': 'application/json' };
        const token = this.getToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        return headers;
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
                navUser.innerHTML = `
                    <span class="navbar-text">
                        <i class="bi bi-person-circle me-1"></i>${user.email || user.username}
                    </span>
                    <button class="btn btn-sm btn-outline-light ms-2" onclick="AUTH.logout()">
                        <i class="bi bi-box-arrow-right me-1"></i>Salir
                    </button>
                `;
            } else {
                navUser.innerHTML = `
                    <a href="login.html" class="btn btn-sm btn-outline-light">
                        <i class="bi bi-box-arrow-in-right me-1"></i>Iniciar Sesión
                    </a>
                `;
            }
        }
    }
};
