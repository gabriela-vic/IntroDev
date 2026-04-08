// static/js/pages/login.js

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const resultado = document.getElementById('resultado');
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('senha');
    
    const inputs = loginForm?.querySelectorAll('input');
    inputs?.forEach(input => {
        input.addEventListener('input', function() {
            if (resultado && resultado.innerHTML) {
                resultado.innerHTML = '';
            }
            this.classList.remove('error');
        });
    });
    
    if (togglePassword && passwordInput) {
        togglePassword.addEventListener('click', function() {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            
            const svg = togglePassword.querySelector('svg');
            if (type === 'text') {
                svg.innerHTML = '<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/>';
            } else {
                svg.innerHTML = '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>';
            }
        });
    }
    
    document.body.addEventListener('htmx:afterSwap', function(event) {
        if (event.detail.target.id === 'resultado') {
            const messageDiv = resultado.querySelector('.result-message');
            if (messageDiv && messageDiv.classList.contains('success')) {
                setTimeout(() => {
                    window.location.href = '/';
                }, 1500);
            }
        }
    });
});