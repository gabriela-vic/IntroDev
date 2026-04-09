// static/js/blog.js

document.addEventListener('htmx:afterSwap', function(detail) {
    // When a new post is loaded, reinitialize HTMX for the navigation buttons
    if (detail.detail.target.id === 'post-detalhes-wrapper') {
        console.log('Post detail loaded, HTMX processing...');
        if (window.htmx) {
            htmx.process(detail.detail.target);
        }
        // Scroll to top of post
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
});

// Smooth scroll when clicking on comments
document.addEventListener('click', function(e) {
    if (e.target.closest('.comments-section')) {
        document.querySelector('.comments-section')?.scrollIntoView({ behavior: 'smooth' });
    }
});
