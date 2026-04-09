// static/js/pages/cadastro.js

document.addEventListener('DOMContentLoaded', function() {
    const cadastroForm = document.getElementById('cadastro-form');
    const resultado = document.getElementById('resultado');
    
    // Validacoes basicas
    function validatePassword(senha, confirmarSenha) {
        if (senha !== confirmarSenha) {
            return { valid: false, message: 'As senhas nao coincidem.' };
        }
        if (senha.length < 3) {
            return { valid: false, message: 'A senha deve ter pelo menos 3 caracteres.' };
        }
        return { valid: true };
    }

    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    // Intercepta o envio para validar antes do HTMX disparar
    if (cadastroForm) {
        cadastroForm.addEventListener('htmx:confirm', function(e) {
            const senha = document.getElementById('senha').value;
            const confirmar = document.getElementById('confirmar_senha').value;
            const email = document.getElementById('email').value;
            const username = document.getElementById('username').value;

            let errorMsg = '';

            if (username.includes(' ')) {
                errorMsg = 'O nome de usuario nao pode conter espacos.';
            } else if (!validateEmail(email)) {
                errorMsg = 'Insira um e-mail valido.';
            } else {
                const passCheck = validatePassword(senha, confirmar);
                if (!passCheck.valid) errorMsg = passCheck.message;
            }

            if (errorMsg) {
                e.preventDefault(); // Impede o envio do HTMX
                resultado.innerHTML = `<p style="color: #b00020; font-size: 0.8rem;">${errorMsg}</p>`;
            }
        });
    }

    // Limpa erro ao digitar
    cadastroForm?.addEventListener('input', function() {
        if (resultado) resultado.innerHTML = '';
    });
});