// Frontend Configuration
// Auto-detects environment and sets API URL accordingly

const CONFIG = (function() {
    const hostname = window.location.hostname;
    
    // Local development
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
        return { API_BASE_URL: '/api' };
    }
    
    // Render.com deployment
    if (hostname.includes('.onrender.com')) {
        return { API_BASE_URL: 'https://ufm-backend-latest.onrender.com/api' };
    }
    
    // Vercel deployment (needs manual backend URL)
    if (hostname.includes('.vercel.app')) {
        // UPDATE THIS with your actual backend URL
        return { API_BASE_URL: 'https://ufm-backend.onrender.com/api' };
    }
    
    // Railway deployment
    if (hostname.includes('.up.railway.app')) {
        return { API_BASE_URL: '/api' };  // Same origin
    }
    
    // Custom domain - UPDATE THIS
    // return { API_BASE_URL: 'https://api.yourdomain.com/api' };
    
    // Fallback to relative URL
    return { API_BASE_URL: '/api' };
})();

// Export for use in other files
window.CONFIG = CONFIG;

console.log('API URL:', CONFIG.API_BASE_URL);


