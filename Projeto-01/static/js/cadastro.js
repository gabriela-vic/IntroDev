// static/js/pages/cadastro.js

document.addEventListener('DOMContentLoaded', function() {
    const cadastroForm = document.getElementById('cadastro-form');
    const resultado = document.getElementById('resultado');
    
    // Função para validar senha
    function validatePassword(senha, confirmarSenha) {
        if (senha !== confirmarSenha) {
            return { valid: false, message: 'As senhas não coincidem!' };
        }
        
        if (senha.length < 3) {
            return { valid: false, message: 'A senha deve ter pelo menos 3 caracteres!' };
        }
        
        return { valid: true, message: '' };
    }
    
    // Função para validar email
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
    
    // Função para validar username (sem espaços)
    function validateUsername(username) {
        return !username.includes(' ') && username.length > 0;
    }
    
    // Validação em tempo real
    const senhaInput = document.getElementById('senha');
    const confirmarSenhaInput = document.getElementById('confirmar_senha');
    const emailInput = document.getElementById('email');
    const usernameInput = document.getElementById('username');
    
    if (senhaInput && confirmarSenhaInput) {
        function checkPasswordMatch() {
            const senha = senhaInput.value;
            const confirmar = confirmarSenhaInput.value;
            
            if (confirmar.length > 0 && senha !== confirmar) {
                confirmarSenhaInput.classList.add('error');
            } else {
                confirmarSenhaInput.classList.remove('error');
            }
        }
        
        senhaInput.addEventListener('input', checkPasswordMatch);
        confirmarSenhaInput.addEventListener('input', checkPasswordMatch);
    }
    
    if (emailInput) {
        emailInput.addEventListener('input', function() {
            if (this.value.length > 0 && !validateEmail(this.value)) {
                this.classList.add('error');
            } else {
                this.classList.remove('error');
            }
        });
    }
    
    if (usernameInput) {
        usernameInput.addEventListener('input', function() {
            if (this.value.includes(' ')) {
                this.classList.add('error');
            } else {
                this.classList.remove('error');
            }
        });
    }
    
    // Toggle para mostrar/esconder senha
    const passwordToggles = document.querySelectorAll('.password-toggle');
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const targetInput = document.getElementById(targetId);
            
            if (targetInput) {
                const type = targetInput.getAttribute('type') === 'password' ? 'text' : 'password';
                targetInput.setAttribute('type', type);
                
                // Trocar ícone
                const svg = this.querySelector('svg');
                if (type === 'text') {
                    svg.innerHTML = '<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/>';
                } else {
                    svg.innerHTML = '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>';
                }
            }
        });
    });
    
    // Validação do formulário antes do envio
    if (cadastroForm) {
        cadastroForm.addEventListener('submit', function(e) {
            const senha = document.getElementById('senha').value;
            const confirmar = document.getElementById('confirmar_senha').value;
            const email = document.getElementById('email').value;
            const username = document.getElementById('username').value;
            
            // Validar senha
            const passwordValidation = validatePassword(senha, confirmar);
            if (!passwordValidation.valid) {
                e.preventDefault();
                resultado.innerHTML = `
                    <div class="result-message error">
                        ${passwordValidation.message}
                    </div>
                `;
                return false;
            }
            
            // Validar email
            if (!validateEmail(email)) {
                e.preventDefault();
                resultado.innerHTML = `
                    <div class="result-message error">
                        Por favor, insira um e-mail válido!
                    </div>
                `;
                return false;
            }
            
            // Validar username
            if (!validateUsername(username)) {
                e.preventDefault();
                resultado.innerHTML = `
                    <div class="result-message error">
                        Nome de usuário não pode conter espaços!
                    </div>
                `;
                return false;
            }
            
            return true;
        });
    }
    
    // Limpar mensagens ao começar a digitar
    const inputs = cadastroForm?.querySelectorAll('input');
    inputs?.forEach(input => {
        input.addEventListener('input', function() {
            if (resultado && resultado.innerHTML) {
                resultado.innerHTML = '';
            }
        });
    });
    
    // Tratar resposta HTMX
    document.body.addEventListener('htmx:afterSwap', function(event) {
        if (event.detail.target.id === 'resultado') {
            const messageDiv = resultado.querySelector('.result-message');
            if (messageDiv && messageDiv.classList.contains('success')) {
                // Se for sucesso, redirecionar para login após 2 segundos
                setTimeout(() => {
                    window.location.href = '/login';
                }, 2000);
            }
        }
    });
});