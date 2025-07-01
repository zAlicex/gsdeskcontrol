document.addEventListener('DOMContentLoaded', function() {
    console.log('=== PAGPENDENTES JS CARREGADO ===');

    // Elementos do DOM
    const form = document.getElementById('pagpendenteForm');
    const formTitle = document.getElementById('form-title');
    const submitBtn = document.getElementById('btn-salvar');
    const pagpendenteIdField = document.getElementById('pagpendente_id');
    const cancelBtn = document.getElementById('cancelEdit');
    const limparBtn = document.getElementById('btn-novo');
    const listContainer = document.getElementById('pagpendente-list-container');
    const localSelect = document.getElementById('id_local');

    console.log('Elementos encontrados:', {
        form: !!form,
        formTitle: !!formTitle,
        submitBtn: !!submitBtn,
        pagpendenteIdField: !!pagpendenteIdField,
        cancelBtn: !!cancelBtn,
        limparBtn: !!limparBtn,
        listContainer: !!listContainer,
        localSelect: !!localSelect
    });

    if (!form || !listContainer || !localSelect) {
        console.error('Elementos essenciais do formulário PagPendente não encontrados!');
        return;
    }

    const CREATE_URL = form.action;
    const UPDATE_URL_TEMPLATE = listContainer.dataset.updateUrlTemplate;
    const GET_URL_TEMPLATE = listContainer.dataset.getUrlTemplate;

    console.log('URLs configuradas:', {
        CREATE_URL,
        UPDATE_URL_TEMPLATE,
        GET_URL_TEMPLATE
    });

    // --- FUNÇÕES ---

    /**
     * Reseta o formulário para o modo de criação.
     */
    function resetFormToCreateMode() {
        console.log('Resetando formulário PagPendente...');
        form.reset();
        pagpendenteIdField.value = '';
        formTitle.textContent = 'Novo Pagamento Pendente';
        submitBtn.textContent = 'Salvar';
        submitBtn.className = 'px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700';
        cancelBtn.style.display = 'none';
        form.action = CREATE_URL;
        form.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
        // Remover seleção de todos os itens
        document.querySelectorAll('.pagpendente-item').forEach(item => {
            item.classList.remove('selected');
        });
    }

    /**
     * Função global para carregar os dados de um pagamento pendente no formulário.
     * @param {string} pagpendenteId - O ID do pagamento pendente.
     */
    window.carregarPagPendente = function(pagpendenteId) {
        console.log(`=== CARREGANDO PAGPENDENTE ID: ${pagpendenteId} ===`);
        const fetchUrl = GET_URL_TEMPLATE.replace('0', pagpendenteId);
        console.log('URL de fetch:', fetchUrl);

        formTitle.textContent = 'Carregando...';
        
        // Remover seleção anterior
        document.querySelectorAll('.pagpendente-item').forEach(item => {
            item.classList.remove('selected');
        });
        
        // Adicionar seleção ao item clicado
        const itemClicado = document.querySelector(`[data-pagpendente-id="${pagpendenteId}"]`);
        if (itemClicado) {
            itemClicado.classList.add('selected');
            console.log('Item selecionado visualmente');
        } else {
            console.warn('Item clicado não encontrado no DOM');
        }
        
        console.log('Fazendo fetch para:', fetchUrl);
        fetch(fetchUrl)
            .then(response => {
                console.log('Response status:', response.status);
                return response.json();
            })
            .then(data => {
                console.log('Dados recebidos:', data);
                
                if (data.success) {
                    const pagpendente = data.pagpendente;
                    console.log('Dados do pagpendente:', pagpendente);
                    
                    // Preenche o formulário com os dados do pagamento pendente
                    pagpendenteIdField.value = pagpendente.id;
                    localSelect.value = pagpendente.local;
                    document.getElementById('id_data_hora').value = pagpendente.data_hora;
                    document.getElementById('id_status').value = pagpendente.status;

                    console.log('Formulário preenchido com:', {
                        id: pagpendenteIdField.value,
                        local: localSelect.value,
                        data_hora: document.getElementById('id_data_hora').value,
                        status: document.getElementById('id_status').value
                    });

                    // Atualiza a UI para o modo de edição
                    formTitle.textContent = 'Editar Pagamento Pendente';
                    submitBtn.textContent = 'Atualizar';
                    form.action = UPDATE_URL_TEMPLATE;
                    cancelBtn.style.display = 'inline-block';
                    form.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    
                    console.log('UI atualizada para modo de edição');
                } else {
                    console.error('Erro na resposta:', data.error);
                    alert(`Erro ao carregar pagamento pendente: ${data.error}`);
                    formTitle.textContent = 'Novo Pagamento Pendente';
                }
            })
            .catch(error => {
                console.error('Erro na requisição:', error);
                alert(`Erro ao carregar pagamento pendente: ${error.message}`);
                formTitle.textContent = 'Novo Pagamento Pendente';
            });
    }

    /**
     * Realiza a busca por AJAX.
     */
    const performSearch = () => {
        const searchQuery = document.querySelector('input[name="q"]').value;
        const resultsContainer = document.getElementById('pagpendente-list-results');
        const searchUrl = `${window.location.pathname}?q=${encodeURIComponent(searchQuery)}`;

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
        console.log('Formulário PagPendente submetido.');
        // Permite o envio padrão do formulário
    });

    // Adicionar evento de busca
    const searchInput = document.querySelector('input[name="q"]');
    if (searchInput) {
        searchInput.addEventListener('input', debouncedSearch);
    }

    console.log('=== PAGPENDENTES JS INICIALIZADO ===');
}); 