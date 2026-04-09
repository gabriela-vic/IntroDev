// static/js/perfil.js

document.addEventListener('DOMContentLoaded', function() {
    // Handle tab switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.dataset.tab;
            
            // Remove active from all buttons and tabs
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            
            // Add active to clicked button and corresponding tab
            btn.classList.add('active');
            const tabContent = document.getElementById(`tab-${tabId}`);
            if (tabContent) {
                tabContent.classList.add('active');
                
                // Trigger HTMX load if not already loaded
                const favGrid = tabContent.querySelector('.favoritos-grid');
                if (favGrid && favGrid.hasAttribute('hx-get')) {
                    htmx.trigger(favGrid, 'load');
                }
            }
        });
    });
});

// Ensure HTMX processes new content in favorites
document.addEventListener('htmx:afterSwap', function(detail) {
    if (detail.detail.target.classList.contains('favoritos-grid')) {
        console.log('Favorites loaded');
        if (window.htmx) {
            htmx.process(detail.detail.target);
        }
    }
});
