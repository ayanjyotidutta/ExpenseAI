// ================================================================ //
// Theme toggle
// ================================================================ //

function initTheme() {
    // Check localStorage for saved theme, default to 'dark'
    const savedTheme = localStorage.getItem('theme') || 'dark';

    // Apply saved theme
    if (savedTheme === 'light') {
        document.documentElement.setAttribute('data-theme', 'light');
        updateThemeIcon('light');
    } else {
        document.documentElement.removeAttribute('data-theme');
        updateThemeIcon('dark');
    }
}

function updateThemeIcon(theme) {
    const icon = document.querySelector('.theme-icon');
    if (icon) {
        icon.textContent = theme === 'light' ? '☀️' : '🌙';
    }
}

function toggleTheme() {
    const htmlElement = document.documentElement;
    const currentTheme = htmlElement.getAttribute('data-theme') || 'dark';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    // Update DOM
    if (newTheme === 'light') {
        htmlElement.setAttribute('data-theme', 'light');
    } else {
        htmlElement.removeAttribute('data-theme');
    }

    // Update localStorage
    localStorage.setItem('theme', newTheme);

    // Update icon
    updateThemeIcon(newTheme);
}

// ================================================================ //
// Video Modal
// ================================================================ //

function openVideoModal() {
    const modal = document.getElementById('video-modal');
    if (modal) {
        modal.classList.add('active');
    }
}

function closeVideoModal() {
    const modal = document.getElementById('video-modal');
    const iframe = document.getElementById('video-iframe');

    if (modal) {
        modal.classList.remove('active');
    }

    // Stop video playback by resetting iframe src
    if (iframe) {
        const src = iframe.src;
        iframe.src = '';
        iframe.src = src;
    }
}

// ================================================================ //
// Initialize on page load
// ================================================================ //

document.addEventListener('DOMContentLoaded', () => {
    // Initialize theme
    initTheme();

    // Attach theme toggle listener
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }

    // Attach video modal listeners
    const videoBtn = document.getElementById('video-btn');
    const videoModal = document.getElementById('video-modal');
    const modalClose = document.getElementById('modal-close');

    if (videoBtn) {
        videoBtn.addEventListener('click', openVideoModal);
    }

    if (modalClose) {
        modalClose.addEventListener('click', closeVideoModal);
    }

    // Close modal when clicking outside the content
    if (videoModal) {
        videoModal.addEventListener('click', (e) => {
            if (e.target === videoModal) {
                closeVideoModal();
            }
        });
    }
});
