// Landing page JavaScript

// Placeholder image as data URL (gray box with image icon)
const PLACEHOLDER_IMAGE = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='450' height='350' viewBox='0 0 450 350'%3E%3Crect fill='%23ddd' width='450' height='350'/%3E%3Ctext fill='%23999' font-family='Arial' font-size='24' x='50%25' y='50%25' text-anchor='middle' dy='.3em'%3EImage%3C/text%3E%3C/svg%3E";

document.addEventListener('DOMContentLoaded', async () => {
    await loadProjects();
    await loadClients();
    setupContactForm();
    setupNewsletterForm();
});

// Load and display projects
async function loadProjects() {
    try {
        const projects = await api.getProjects();
        const projectsContainer = document.getElementById('projects-container');
        
        if (!projectsContainer) return;

        if (projects.length === 0) {
            projectsContainer.innerHTML = '<div class="empty-state">No projects available.</div>';
            return;
        }

        projectsContainer.innerHTML = projects.map(project => `
            <div class="project-card">
                <img src="${project.image_url}" alt="${project.name}" onerror="this.onerror=null; this.src='${PLACEHOLDER_IMAGE}'">
                <div class="project-info">
                    <h3>${escapeHtml(project.name)}</h3>
                    <p>${escapeHtml(project.description)}</p>
                    <button class="read-more-btn">Read More</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading projects:', error);
        const projectsContainer = document.getElementById('projects-container');
        if (projectsContainer) {
            projectsContainer.innerHTML = '<p>Error loading projects. Please try again later.</p>';
        }
    }
}

// Load and display clients
async function loadClients() {
    try {
        const clients = await api.getClients();
        const clientsContainer = document.getElementById('clients-container');
        
        if (!clientsContainer) return;

        if (clients.length === 0) {
            clientsContainer.innerHTML = '<div class="empty-state">No clients available.</div>';
            return;
        }

        clientsContainer.innerHTML = clients.map(client => `
            <div class="client-card">
                <img src="${client.image_url}" alt="${client.name}" onerror="this.onerror=null; this.src='${PLACEHOLDER_IMAGE}'">
                <p class="client-description">${escapeHtml(client.description)}</p>
                <h4 class="client-name">${escapeHtml(client.name)}</h4>
                <p class="client-designation">${escapeHtml(client.designation)}</p>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading clients:', error);
        const clientsContainer = document.getElementById('clients-container');
        if (clientsContainer) {
            clientsContainer.innerHTML = '<p>Error loading clients. Please try again later.</p>';
        }
    }
}

// Setup contact form
function setupContactForm() {
    const contactForm = document.getElementById('contact-form');
    if (!contactForm) return;

    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = {
            full_name: document.getElementById('full-name').value.trim(),
            email: document.getElementById('email').value.trim(),
            mobile_number: document.getElementById('mobile-number').value.trim(),
            city: document.getElementById('city').value.trim(),
        };

        // Validation
        if (!formData.full_name || !formData.email || !formData.mobile_number || !formData.city) {
            showMessage('Please fill in all fields.', 'error');
            return;
        }

        if (!isValidEmail(formData.email)) {
            showMessage('Please enter a valid email address.', 'error');
            return;
        }

        try {
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Submitting...';

            await api.submitContact(formData);
            showMessage('Thank you! Your message has been submitted successfully.', 'success');
            contactForm.reset();
        } catch (error) {
            showMessage('Failed to submit form. Please try again.', 'error');
        } finally {
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Submit';
        }
    });
}

// Setup newsletter form
function setupNewsletterForm() {
    const newsletterForm = document.getElementById('newsletter-form');
    if (!newsletterForm) return;

    newsletterForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('newsletter-email').value.trim();

        if (!email) {
            showMessage('Please enter your email address.', 'error');
            return;
        }

        if (!isValidEmail(email)) {
            showMessage('Please enter a valid email address.', 'error');
            return;
        }

        try {
            const subscribeBtn = newsletterForm.querySelector('button[type="submit"]');
            subscribeBtn.disabled = true;
            subscribeBtn.textContent = 'Subscribing...';

            await api.subscribeNewsletter(email);
            showMessage('Successfully subscribed to newsletter!', 'success');
            newsletterForm.reset();
        } catch (error) {
            showMessage('Failed to subscribe. Please try again.', 'error');
        } finally {
            const subscribeBtn = newsletterForm.querySelector('button[type="submit"]');
            subscribeBtn.disabled = false;
            subscribeBtn.textContent = 'Subscribe';
        }
    });
}

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showMessage(message, type = 'info') {
    // Create or update message element
    let messageEl = document.getElementById('message');
    if (!messageEl) {
        messageEl = document.createElement('div');
        messageEl.id = 'message';
        document.body.appendChild(messageEl);
    }

    messageEl.textContent = message;
    messageEl.className = `message message-${type}`;
    messageEl.style.display = 'block';

    // Auto-hide after 5 seconds
    setTimeout(() => {
        messageEl.style.display = 'none';
    }, 5000);
}

