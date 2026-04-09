// static/js/htmx_config.js

// Configure HTMX with logging for debugging
document.addEventListener('htmx:configRequest', function(detail) {
    console.log('HTMX Request:', detail.detail.xhr.responseURL);
});

document.addEventListener('htmx:responseError', function(detail) {
    console.error('HTMX Response Error:', detail.detail.xhr.status, detail.detail.xhr.statusText);
});

document.addEventListener('htmx:swapError', function(detail) {
    console.error('HTMX Swap Error:', detail.detail.error);
});

// Ensure HTMX processes new content after swap
document.addEventListener('htmx:afterSwap', function(detail) {
    console.log('HTMX Swap completed for:', detail.detail.target.id);
    // Force HTMX to process any new elements with HTMX attributes
    if (window.htmx) {
        htmx.process(detail.detail.target);
        console.log('HTMX process called on target');
    }
});

document.addEventListener('htmx:afterSettle', function(detail) {
    console.log('HTMX Settle completed');
});

