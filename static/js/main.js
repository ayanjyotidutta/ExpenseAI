// Theme toggle
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

// Initialize theme on page load
document.addEventListener('DOMContentLoaded', () => {
    initTheme();

    // Attach toggle listener
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
});
