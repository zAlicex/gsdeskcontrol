document.addEventListener('DOMContentLoaded', function() {
    console.log('=== CLIENTES JS CARREGADO ===');

    // Elementos do DOM
    const form = document.getElementById('clienteForm');
    const formTitle = document.getElementById('formTitle');
    const submitBtn = document.getElementById('submitBtn');
    const clienteIdField = document.getElementById('cliente_id');
    const cancelBtn = document.getElementById('cancelEdit');
    const limparBtn = document.getElementById('limparForm');
    const listContainer = document.getElementById('client-list-container');
    const nomeInput = document.getElementById('nome');

    if (!form || !listContainer || !nomeInput) {
        console.error('Elementos essenciais do formulário Cliente não encontrados!');
        return;
    }

    const CREATE_URL = form.action;
    const UPDATE_URL_TEMPLATE = listContainer.dataset.updateUrlTemplate;

    // --- FUNÇÕES ---

    /**
     * Reseta o formulário para o modo de criação.
     */
    function resetFormToCreateMode() {
        console.log('Resetando formulário Cliente...');
        form.reset();
        clienteIdField.value = '';
        formTitle.textContent = 'Novo Local';
        submitBtn.textContent = 'Salvar';
        submitBtn.className = 'btn-primary';
        cancelBtn.style.display = 'none';
        form.action = CREATE_URL;
        form.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
        // Remover seleção de todos os itens
        document.querySelectorAll('.cliente-item').forEach(item => {
            item.classList.remove('selected');
        });
    }

    /**
     * Função global para carregar os dados de um cliente no formulário.
     * @param {string} clienteId - O ID do cliente.
     */
    window.carregarCliente = function(clienteId) {
        console.log(`Carregando Cliente ID: ${clienteId}`);
        const GET_CLIENT_URL_TEMPLATE = listContainer.dataset.getUrlTemplate;
        const fetchUrl = GET_CLIENT_URL_TEMPLATE.replace('0', clienteId);

        formTitle.textContent = 'Carregando...';
        
        // Remover seleção anterior
        document.querySelectorAll('.cliente-item').forEach(item => {
            item.classList.remove('selected');
        });
        
        // Adicionar seleção ao item clicado
        const itemClicado = document.querySelector(`[data-cliente-id="${clienteId}"]`);
        if (itemClicado) {
            itemClicado.classList.add('selected');
        }
        
        fetch(fetchUrl)
            .then(response => response.json())
            .then(data => {
                console.log('Dados recebidos:', data);
                
                if (data.success) {
                    const cliente = data.cliente;
                    
                    // Preenche o formulário com os dados do cliente
                    clienteIdField.value = cliente.id;
                    nomeInput.value = cliente.nome || '';

                    // Atualiza a UI para o modo de edição
                    formTitle.textContent = `Editar Local: ${cliente.nome}`;
                    submitBtn.textContent = 'Atualizar';
                    form.action = UPDATE_URL_TEMPLATE.replace('0', cliente.id);
                    cancelBtn.style.display = 'inline-block';
                    form.scrollIntoView({ behavior: 'smooth', block: 'start' });
                } else {
                    alert(`Erro ao carregar cliente: ${data.error}`);
                    formTitle.textContent = 'Novo Local';
                }
            })
            .catch(error => {
                console.error('Erro na requisição:', error);
                alert(`Erro ao carregar cliente: ${error.message}`);
                formTitle.textContent = 'Novo Local';
            });
    }

    /**
     * Realiza a busca por AJAX.
     */
    const performSearch = () => {
        const searchQuery = document.querySelector('input[name="search_name"]').value;
        const resultsContainer = document.getElementById('client-list-results');
        const searchUrl = `${window.location.pathname}?search_name=${encodeURIComponent(searchQuery)}`;

        resultsContainer.innerHTML = '<div class="p-6 text-center text-gray-500">Buscando...</div>';

        fetch(searchUrl, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => response.text())
        .then(html => {
            resultsContainer.innerHTML = html;
        })
        .catch(error => {
            console.error('Erro na busca AJAX:', error);
            resultsContainer.innerHTML = '<div class="p-6 text-center text-red-500">Erro ao buscar resultados.</div>';
        });
    };

    const debounce = (func, delay) => {
        let timeoutId;
        return (...args) => {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => {
                func.apply(this, args);
            }, delay);
        };
    };
    const debouncedSearch = debounce(performSearch, 300);

    // --- EVENT LISTENERS ---

    if (limparBtn) limparBtn.addEventListener('click', resetFormToCreateMode);
    if (cancelBtn) cancelBtn.addEventListener('click', () => window.location.reload());

    form.addEventListener('submit', function() {
        console.log('Formulário Cliente submetido.');
        // Permite o envio padrão do formulário
    });

    // Adicionar evento de busca
    const searchInput = document.querySelector('input[name="search_name"]');
    if (searchInput) {
        searchInput.addEventListener('input', debouncedSearch);
    }

    console.log('=== CLIENTES JS INICIALIZADO ===');
}); 