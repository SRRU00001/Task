// Admin panel JavaScript

// Placeholder image as data URL
const PLACEHOLDER_IMAGE = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='450' height='350' viewBox='0 0 450 350'%3E%3Crect fill='%23ddd' width='450' height='350'/%3E%3Ctext fill='%23999' font-family='Arial' font-size='24' x='50%25' y='50%25' text-anchor='middle' dy='.3em'%3EImage%3C/text%3E%3C/svg%3E";

let currentEditingProject = null;
let currentEditingClient = null;

document.addEventListener('DOMContentLoaded', async () => {
    // Check authentication
    await checkAuth();
    
    // Setup event listeners
    setupAuth();
    setupProjectManagement();
    setupClientManagement();
    setupContactView();
    setupNewsletterView();
});

// Check authentication status
async function checkAuth() {
    try {
        await api.verifyAdmin();
        showAdminPanel();
    } catch (error) {
        showLoginScreen();
    }
}

// Show login screen
function showLoginScreen() {
    document.getElementById('login-screen').style.display = 'block';
    document.getElementById('admin-panel').style.display = 'none';
}

// Show admin panel
function showAdminPanel() {
    document.getElementById('login-screen').style.display = 'none';
    document.getElementById('admin-panel').style.display = 'block';
    loadAdminData();
}

// Setup authentication
function setupAuth() {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value.trim();
            const errorDiv = document.getElementById('login-error');

            if (!username || !password) {
                errorDiv.textContent = 'Please enter both username and password';
                errorDiv.style.display = 'block';
                return;
            }

            try {
                const response = await api.login(username, password);
                api.setToken(response.access_token);
                await checkAuth();
            } catch (error) {
                errorDiv.textContent = error.message || 'Invalid username or password';
                errorDiv.style.display = 'block';
            }
        });
    }

    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            api.setToken(null);
            showLoginScreen();
            document.getElementById('login-form').reset();
            document.getElementById('login-error').style.display = 'none';
        });
    }
}

// Load all admin data
async function loadAdminData() {
    await loadProjectsAdmin();
    await loadClientsAdmin();
    await loadContacts();
    await loadNewsletters();
}

// Project Management
function setupProjectManagement() {
    const projectForm = document.getElementById('project-form');
    if (projectForm) {
        projectForm.addEventListener('submit', handleProjectSubmit);
    }

    const projectFormReset = document.getElementById('project-form-reset');
    if (projectFormReset) {
        projectFormReset.addEventListener('click', () => {
            document.getElementById('project-form').reset();
            currentEditingProject = null;
            document.getElementById('project-form-title').textContent = 'Add New Project';
        });
    }
}

async function handleProjectSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('name', document.getElementById('project-name').value.trim());
    formData.append('description', document.getElementById('project-description').value.trim());
    
    const imageFile = document.getElementById('project-image').files[0];
    if (!imageFile && !currentEditingProject) {
        alert('Please select an image');
        return;
    }
    if (imageFile) {
        formData.append('image', imageFile);
    }

    try {
        if (currentEditingProject) {
            await api.updateProject(currentEditingProject.id, formData);
            showMessage('Project updated successfully!', 'success');
        } else {
            await api.createProject(formData);
            showMessage('Project created successfully!', 'success');
        }
        
        document.getElementById('project-form').reset();
        currentEditingProject = null;
        document.getElementById('project-form-title').textContent = 'Add New Project';
        await loadProjectsAdmin();
    } catch (error) {
        showMessage('Failed to save project: ' + error.message, 'error');
    }
}

async function loadProjectsAdmin() {
    try {
        const projects = await api.getProjects();
        const container = document.getElementById('projects-list');
        if (!container) return;

        if (projects.length === 0) {
            container.innerHTML = '<p>No projects yet.</p>';
            return;
        }

        container.innerHTML = projects.map(project => `
            <div class="admin-item-card">
                <img src="${project.image_url}" alt="${project.name}" onerror="this.onerror=null; this.src='${PLACEHOLDER_IMAGE}'">
                <div class="admin-item-info">
                    <h4>${escapeHtml(project.name)}</h4>
                    <p>${escapeHtml(project.description)}</p>
                </div>
                <div class="admin-item-actions">
                    <button onclick="editProject('${project.id}', '${escapeHtml(project.name)}', '${escapeHtml(project.description)}')">Edit</button>
                    <button onclick="deleteProject('${project.id}')" class="delete-btn">Delete</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading projects:', error);
    }
}

async function editProject(id, name, description) {
    currentEditingProject = { id, name, description };
    document.getElementById('project-name').value = name;
    document.getElementById('project-description').value = description;
    document.getElementById('project-form-title').textContent = 'Edit Project';
    document.getElementById('project-form').scrollIntoView({ behavior: 'smooth' });
}

async function deleteProject(id) {
    if (!confirm('Are you sure you want to delete this project?')) return;

    try {
        await api.deleteProject(id);
        showMessage('Project deleted successfully!', 'success');
        await loadProjectsAdmin();
    } catch (error) {
        showMessage('Failed to delete project: ' + error.message, 'error');
    }
}

// Client Management
function setupClientManagement() {
    const clientForm = document.getElementById('client-form');
    if (clientForm) {
        clientForm.addEventListener('submit', handleClientSubmit);
    }

    const clientFormReset = document.getElementById('client-form-reset');
    if (clientFormReset) {
        clientFormReset.addEventListener('click', () => {
            document.getElementById('client-form').reset();
            currentEditingClient = null;
            document.getElementById('client-form-title').textContent = 'Add New Client';
        });
    }
}

async function handleClientSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('name', document.getElementById('client-name').value.trim());
    formData.append('description', document.getElementById('client-description').value.trim());
    formData.append('designation', document.getElementById('client-designation').value.trim());
    
    const imageFile = document.getElementById('client-image').files[0];
    if (!imageFile && !currentEditingClient) {
        alert('Please select an image');
        return;
    }
    if (imageFile) {
        formData.append('image', imageFile);
    }

    try {
        if (currentEditingClient) {
            await api.updateClient(currentEditingClient.id, formData);
            showMessage('Client updated successfully!', 'success');
        } else {
            await api.createClient(formData);
            showMessage('Client created successfully!', 'success');
        }
        
        document.getElementById('client-form').reset();
        currentEditingClient = null;
        document.getElementById('client-form-title').textContent = 'Add New Client';
        await loadClientsAdmin();
    } catch (error) {
        showMessage('Failed to save client: ' + error.message, 'error');
    }
}

async function loadClientsAdmin() {
    try {
        const clients = await api.getClients();
        const container = document.getElementById('clients-list');
        if (!container) return;

        if (clients.length === 0) {
            container.innerHTML = '<p>No clients yet.</p>';
            return;
        }

        container.innerHTML = clients.map(client => `
            <div class="admin-item-card">
                <img src="${client.image_url}" alt="${client.name}" onerror="this.onerror=null; this.src='${PLACEHOLDER_IMAGE}'">
                <div class="admin-item-info">
                    <h4>${escapeHtml(client.name)}</h4>
                    <p>${escapeHtml(client.description)}</p>
                    <p><strong>Designation:</strong> ${escapeHtml(client.designation)}</p>
                </div>
                <div class="admin-item-actions">
                    <button onclick="editClient('${client.id}', '${escapeHtml(client.name)}', '${escapeHtml(client.description)}', '${escapeHtml(client.designation)}')">Edit</button>
                    <button onclick="deleteClient('${client.id}')" class="delete-btn">Delete</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading clients:', error);
    }
}

async function editClient(id, name, description, designation) {
    currentEditingClient = { id, name, description, designation };
    document.getElementById('client-name').value = name;
    document.getElementById('client-description').value = description;
    document.getElementById('client-designation').value = designation;
    document.getElementById('client-form-title').textContent = 'Edit Client';
    document.getElementById('client-form').scrollIntoView({ behavior: 'smooth' });
}

async function deleteClient(id) {
    if (!confirm('Are you sure you want to delete this client?')) return;

    try {
        await api.deleteClient(id);
        showMessage('Client deleted successfully!', 'success');
        await loadClientsAdmin();
    } catch (error) {
        showMessage('Failed to delete client: ' + error.message, 'error');
    }
}

// Contact View
function setupContactView() {
    // Contacts are loaded in loadAdminData
}

async function loadContacts() {
    try {
        const contacts = await api.getContacts();
        const container = document.getElementById('contacts-list');
        if (!container) return;

        if (contacts.length === 0) {
            container.innerHTML = '<p>No contact submissions yet.</p>';
            return;
        }

        container.innerHTML = `
            <table class="admin-table">
                <thead>
                    <tr>
                        <th>Full Name</th>
                        <th>Email</th>
                        <th>Mobile Number</th>
                        <th>City</th>
                        <th>Submitted At</th>
                    </tr>
                </thead>
                <tbody>
                    ${contacts.map(contact => `
                        <tr>
                            <td>${escapeHtml(contact.full_name)}</td>
                            <td>${escapeHtml(contact.email)}</td>
                            <td>${escapeHtml(contact.mobile_number)}</td>
                            <td>${escapeHtml(contact.city)}</td>
                            <td>${new Date(contact.created_at).toLocaleString()}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    } catch (error) {
        console.error('Error loading contacts:', error);
    }
}

// Newsletter View
function setupNewsletterView() {
    // Newsletters are loaded in loadAdminData
}

async function loadNewsletters() {
    try {
        const newsletters = await api.getNewsletters();
        const container = document.getElementById('newsletters-list');
        if (!container) return;

        if (newsletters.length === 0) {
            container.innerHTML = '<p>No newsletter subscriptions yet.</p>';
            return;
        }

        container.innerHTML = `
            <div class="newsletter-list">
                ${newsletters.map(newsletter => `
                    <div class="newsletter-item">
                        <span class="newsletter-email">${escapeHtml(newsletter.email)}</span>
                        <span class="newsletter-date">${new Date(newsletter.subscribed_at).toLocaleString()}</span>
                    </div>
                `).join('')}
            </div>
        `;
    } catch (error) {
        console.error('Error loading newsletters:', error);
    }
}

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML.replace(/'/g, "&#39;").replace(/"/g, "&quot;");
}

function showMessage(message, type = 'info') {
    const messageEl = document.getElementById('admin-message');
    if (messageEl) {
        messageEl.textContent = message;
        messageEl.className = `admin-message admin-message-${type}`;
        messageEl.style.display = 'block';
        setTimeout(() => {
            messageEl.style.display = 'none';
        }, 5000);
    }
}

// Make functions available globally
window.editProject = editProject;
window.deleteProject = deleteProject;
window.editClient = editClient;
window.deleteClient = deleteClient;

