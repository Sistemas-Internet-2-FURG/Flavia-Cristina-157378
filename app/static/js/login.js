document.addEventListener('DOMContentLoaded', function () {
    // Verifique se os botões de registrar e entrar existem
    const registrarButton = document.getElementById("registrar");
    const entrarButton = document.getElementById("entrar");

    // Adiciona o listener de evento se o elemento existir
    if (registrarButton) {
        registrarButton.addEventListener("click", function () {
            document.getElementById("container").classList.add("right-panel-active");
        });
    } else {
        console.error("Botão de registrar não encontrado!");
    }

    if (entrarButton) {
        entrarButton.addEventListener("click", function () {
            document.getElementById("container").classList.remove("right-panel-active");
        });
    } else {
        console.error("Botão de entrar não encontrado!");
    }

    // Verifique se o formulário de registro existe antes de adicionar o evento
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async function(event) {
            event.preventDefault();

            // Verifique se os campos realmente existem
            const nomeInput = document.getElementById('nome');
            const emailInput = document.getElementById('email');
            const senhaInput = document.getElementById('senha');
            const confirmarSenhaInput = document.getElementById('confirmar_senha');

            if (!nomeInput || !emailInput || !senhaInput || !confirmarSenhaInput) {
                console.error('Campos do formulário não encontrados!');
                return;
            }

            const nome = nomeInput.value;
            const email = emailInput.value;
            const senha = senhaInput.value;
            const confirmarSenha = confirmarSenhaInput.value;

            // Verificação simples das senhas
            if (senha !== confirmarSenha) {
                alert('As senhas não coincidem!');
                return;
            }

            try {
                const response = await axios.post('/register', {
                    username: nome,
                    email: email,
                    password: senha
                }, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                if (response.status === 201) {
                    alert('Cadastro realizado com sucesso!');
                    window.location.href = '/login';  // Redireciona para a página de login
                }
            } catch (error) {
                console.error('Erro no registro:', error);
                alert('Erro ao registrar! Verifique os dados e tente novamente.');
            }
        });
    } else {
        console.error("Formulário de registro não encontrado!");
    }
});
