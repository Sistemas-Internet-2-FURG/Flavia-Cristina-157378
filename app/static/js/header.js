// header.js
document.addEventListener("DOMContentLoaded", function() {
    const authButtonsDiv = document.getElementById("auth-buttons");
  
    // Verificar se o usuário está logado via Axios
    axios.get('/restapi/check-login')  // Supondo que haja uma API que retorna o estado de login
      .then(response => {
        if (response.data.loggedIn) {
          authButtonsDiv.innerHTML = `
            <button id="logout-btn">Sair</button>
          `;
          document.getElementById("logout-btn").addEventListener('click', logout);
        } else {
          authButtonsDiv.innerHTML = `
            <a href="/login"><button>Log in</button></a>
            <a href="/register"><button>Registrar</button></a>
          `;
        }
      })
      .catch(error => {
        console.error("Erro ao verificar login:", error);
        authButtonsDiv.innerHTML = `
          <a href="/login"><button>Log in</button></a>
          <a href="/register"><button>Registrar</button></a>
        `;
      });
  
    // Função para fazer logout
    function logout() {
      axios.post('/restapi/logout')  // Supondo que haja uma API para realizar o logout
        .then(response => {
          window.location.reload();  // Recarregar a página após o logout
        })
        .catch(error => {
          console.error("Erro ao fazer logout:", error);
        });
    }
  });
  