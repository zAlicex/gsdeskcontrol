document.addEventListener('DOMContentLoaded', function() {
    console.log('=== RAT JS CARREGADO ===');

    // Elementos do DOM
    const form = document.getElementById('ratForm');
    const formTitle = document.getElementById('formTitle');
    const submitBtn = document.getElementById('submitBtn');
    const ratIdField = document.getElementById('rat_id');
    const cancelBtn = document.getElementById('cancelEdit');
    const limparBtn = document.getElementById('limparForm');
    const listContainer = document.getElementById('rat-list-container');
    const localSelect = document.getElementById('local');

    if (!form || !listContainer || !localSelect) {
        console.error('Elementos essenciais do formulário RAT não encontrados!');
        return;
    }

    const CREATE_URL = form.action;
    const UPDATE_URL_TEMPLATE = listContainer.dataset.updateUrlTemplate;

    // --- FUNÇÕES ---

    /**
     * Reseta o formulário para o modo de criação.
     */
    function resetFormToCreateMode() {
        console.log('Resetando formulário RAT...');
        form.reset();
        ratIdField.value = '';
        formTitle.textContent = 'Novo RAT';
        submitBtn.textContent = 'Salvar';
        submitBtn.className = 'btn-primary';
        cancelBtn.style.display = 'none';
        form.action = CREATE_URL;
        form.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    /**
     * Função global para carregar os dados de um RAT no formulário.
     * @param {string} ratId - O ID do RAT.
     */
    window.carregarRat = function(ratId) {
        console.log(`Carregando RAT ID: ${ratId}`);
        const GET_RAT_URL_TEMPLATE = listContainer.dataset.getUrlTemplate;
        const fetchUrl = GET_RAT_URL_TEMPLATE.replace('0', ratId);

        formTitle.textContent = 'Carregando...';
        
        fetch(fetchUrl)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const rat = data.rat;
                    // Preenche os campos reais do modelo
                    if (localSelect) localSelect.value = rat.local_id;
                    document.getElementById('nome').value = rat.nome || '';
                    document.getElementById('cpf').value = rat.cpf || '';

                    // Atualiza a UI para o modo de edição
                    ratIdField.value = rat.id;
                    formTitle.textContent = `Editar RAT: ${rat.nome}`;
                    submitBtn.textContent = 'Atualizar';
                    form.action = UPDATE_URL_TEMPLATE.replace('0', rat.id);
                    cancelBtn.style.display = 'inline-block';
                    form.scrollIntoView({ behavior: 'smooth', block: 'start' });
                } else {
                    alert(`Erro ao carregar RAT: ${data.error}`);
                    formTitle.textContent = 'Novo RAT';
                }
            })
            .catch(error => {
                console.error('Erro na requisição:', error);
                alert(`Erro ao carregar RAT: ${error.message}`);
                formTitle.textContent = 'Novo RAT';
            });
    }

    /**
     * Busca e preenche os dados do cliente selecionado.
     * @param {string} clienteId - O ID do cliente.
     */
    function fetchAndFillClienteData(clienteId) {
        if (!clienteId) {
            resetFormToCreateMode(); // Se des-selecionar, limpa tudo
            return;
        }

        const fetchUrl = GET_CLIENT_URL_TEMPLATE.replace('0', clienteId);
        
        fetch(fetchUrl)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const cliente = data.cliente;
                    document.getElementById('cliente_nome').value = cliente.nome || '';
                    document.getElementById('cliente_cpf_cnpj').value = cliente.cpf_cnpj || '';
                    document.getElementById('cliente_telefone').value = cliente.telefone || '';
                    document.getElementById('cliente_celular').value = cliente.celular || '';
                    document.getElementById('cliente_email').value = cliente.email || '';
                    document.getElementById('cliente_endereco').value = cliente.endereco || '';
                    document.getElementById('cliente_bairro').value = cliente.bairro || '';
                    document.getElementById('cliente_cidade').value = cliente.cidade || '';
                    document.getElementById('cliente_cep').value = cliente.cep || '';
                } else {
                    alert('Erro ao buscar dados do cliente.');
                }
            })
            .catch(error => console.error('Erro ao buscar dados do cliente:', error));
    }

    /**
     * Realiza a busca por AJAX.
     */
    const performSearch = () => {
        const searchName = document.getElementById('search-name-input').value;
        const searchRat = document.getElementById('search-rat-input').value;
        const resultsContainer = document.getElementById('rat-list-results');
        const searchUrl = `${window.location.pathname}?search_name=${encodeURIComponent(searchName)}&search_rat=${encodeURIComponent(searchRat)}`;

        resultsContainer.innerHTML = '<div class="p-6 text-center text-gray-500">Buscando...</div>';

        fetch(searchUrl, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => response.json())
        .then(data => {
            resultsContainer.innerHTML = data.html;
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
        console.log('Formulário RAT submetido.');
        // Permite o envio padrão do formulário
    });

    console.log('=== RAT JS INICIALIZADO ===');
}); 