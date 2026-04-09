// static/js/search.js

document.addEventListener('DOMContentLoaded', function() {
    const searchBtn = document.getElementById('searchBtn');
    const searchDropdown = document.getElementById('searchDropdown');
    const searchInput = document.getElementById('searchInput');
    
    if (!searchBtn) return;
    
    // Toggle search dropdown
    searchBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        searchDropdown.classList.toggle('active');
        if (searchDropdown.classList.contains('active')) {
            searchInput.focus();
        }
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.search-wrapper')) {
            searchDropdown.classList.remove('active');
        }
    });
    
    // Prevent dropdown from closing when clicking inside it
    searchDropdown.addEventListener('click', (e) => {
        e.stopPropagation();
    });
    
    // Clear search when clicking a result (HTMX will navigate)
    document.addEventListener('htmx:afterSwap', function(detail) {
        if (detail.detail.target.id === 'search-results') {
            // Search results were updated, check if user clicked a result
            const results = detail.detail.target.querySelectorAll('.search-result-item');
            results.forEach(result => {
                result.addEventListener('click', () => {
                    // Close search after clicking result
                    setTimeout(() => {
                        searchDropdown.classList.remove('active');
                        searchInput.value = '';
                    }, 100);
                });
            });
        }
    });
});
