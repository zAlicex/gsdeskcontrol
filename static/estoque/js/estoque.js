document.addEventListener('DOMContentLoaded', function() {
    console.log('=== JAVASCRIPT CARREGADO ===');
    
    // Elementos do DOM
    const form = document.getElementById('estoqueForm');
    const formTitle = document.getElementById('formTitle');
    const submitBtn = document.getElementById('submitBtn');
    const estoqueIdField = document.getElementById('estoque_id');
    const cancelBtn = document.getElementById('cancelEdit');
    const limparBtn = document.getElementById('limparForm');
    const listContainer = document.getElementById('estoque-list-container');

    console.log('Elementos encontrados:', {
        form: !!form,
        formTitle: !!formTitle,
        submitBtn: !!submitBtn,
        estoqueIdField: !!estoqueIdField,
        listContainer: !!listContainer
    });

    if (!form || !listContainer) {
        console.error('Elementos essenciais não encontrados!');
        return;
    }

    const CREATE_URL = form.action;
    const UPDATE_URL_TEMPLATE = listContainer.dataset.updateUrlTemplate;
    const GET_ESTOQUE_URL_TEMPLATE = listContainer.dataset.getUrlTemplate;
    
    console.log('URLs configuradas:', {
        CREATE_URL,
        UPDATE_URL_TEMPLATE,
        GET_ESTOQUE_URL_TEMPLATE
    });

    // Função para obter o token CSRF
    function getCSRFToken() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfToken ? csrfToken.value : '';
    }

    /**
     * Reseta o formulário para o estado de criação de forma explícita.
     */
    function resetFormToCreateMode() {
        console.log('Botão Voltar/Limpar clicado. Resetando formulário...');

        // Reseta o formulário
        if(form) form.reset();

        // Reseta os campos e botões específicos da interface
        if(estoqueIdField) estoqueIdField.value = '';
        if(formTitle) formTitle.textContent = 'Novo Registro';
        if(submitBtn) {
            submitBtn.textContent = 'Salvar';
            submitBtn.className = 'btn-primary';
        }
        if(cancelBtn) cancelBtn.style.display = 'none';

        // Reseta a URL de action do formulário para a URL de criação
        if (form && CREATE_URL) {
            form.action = CREATE_URL;
        }

        console.log('Formulário resetado para o modo de criação.');
        
        // Rola a página para o topo do formulário para melhor UX
        if (form) form.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    /**
     * Função global para carregar os dados de um estoque no formulário.
     * @param {string} estoqueId - O ID do estoque.
     */
    window.carregarEstoque = function(estoqueId) {
        console.log(`Carregando estoque ID: ${estoqueId}`);
        const fetchUrl = GET_ESTOQUE_URL_TEMPLATE.replace('0', estoqueId);

        formTitle.textContent = 'Carregando...';
        
        fetch(fetchUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    const estoque = data.estoque;
                    
                    // Preenche os campos do formulário
                    if (estoqueIdField) estoqueIdField.value = estoque.id;
                    
                    // Preenche os campos específicos do modelo Estoque
                    const localSelect = document.querySelector('select[name="local"]');
                    if (localSelect && estoque.local_id) {
                        localSelect.value = estoque.local_id;
                    }
                    
                    const usuarioSelect = document.querySelector('select[name="usuario"]');
                    if (usuarioSelect && estoque.usuario_id) {
                        usuarioSelect.value = estoque.usuario_id;
                    }
                    
                    const dataHoraInput = document.querySelector('input[name="data_hora"]');
                    if (dataHoraInput && estoque.data_hora) {
                        dataHoraInput.value = estoque.data_hora;
                    }
                    
                    const statusSelect = document.querySelector('select[name="status"]');
                    if (statusSelect && estoque.status) {
                        statusSelect.value = estoque.status;
                    }

                    // Atualiza a UI para o modo de edição
                    formTitle.textContent = `Editar Registro: ${estoque.id}`;
                    submitBtn.textContent = 'Atualizar';
                    form.action = UPDATE_URL_TEMPLATE.replace('0', estoque.id);
                    cancelBtn.style.display = 'inline-block';
                    form.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    
                    console.log('Estoque carregado com sucesso:', estoque);
                } else {
                    console.error('Erro ao carregar estoque:', data.error);
                    alert(`Erro ao carregar estoque: ${data.error}`);
                    formTitle.textContent = 'Novo Registro';
                }
            })
            .catch(error => {
                console.error('Erro na requisição:', error);
                alert(`Erro ao carregar estoque: ${error.message}`);
                formTitle.textContent = 'Novo Registro';
            });
    }

    // Event listeners
    if (limparBtn) limparBtn.addEventListener('click', resetFormToCreateMode);

    // O botão "Voltar" (cancelBtn) agora simplesmente recarrega a página.
    if (cancelBtn) {
        cancelBtn.addEventListener('click', function() {
            console.log('Botão Voltar clicado. Recarregando a página...');
            window.location.reload();
        });
    }

    /**
     * Lida com a submissão do formulário.
     */
    form.addEventListener('submit', function(e) {
        console.log('Formulário submetido - redirecionamento normal');
        
        // Remove o preventDefault para permitir o submit normal
        // e.preventDefault();
        
        // Adiciona CSRF token se necessário
        const csrfToken = getCSRFToken();
        if (csrfToken && !form.querySelector('[name=csrfmiddlewaretoken]')) {
            const csrfInput = document.createElement('input');
            csrfInput.type = 'hidden';
            csrfInput.name = 'csrfmiddlewaretoken';
            csrfInput.value = csrfToken;
            form.appendChild(csrfInput);
        }
        
        // O formulário será submetido normalmente e a página será redirecionada
        // A view do Django irá processar e redirecionar de volta para a mesma página
    });

    // --- BUSCA INSTANTÂNEA ---
    const searchLocalInput = document.getElementById('search-local-input');
    const searchUsuarioInput = document.getElementById('search-usuario-input');
    const searchStatusInput = document.getElementById('search-status-input');
    const listResults = document.getElementById('estoque-list-results');

    function debounce(func, wait) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }

    function filtrarLista() {
        const local = searchLocalInput ? searchLocalInput.value : '';
        const usuario = searchUsuarioInput ? searchUsuarioInput.value : '';
        const status = searchStatusInput ? searchStatusInput.value : '';
        
        const params = new URLSearchParams({
            search_local: local,
            search_usuario: usuario,
            search_status: status
        });

        fetch(window.location.pathname + '?' + params.toString(), {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.html && listResults) {
                listResults.innerHTML = data.html;
            }
        });
    }

    const debouncedFiltrarLista = debounce(filtrarLista, 300);

    if (searchLocalInput) searchLocalInput.addEventListener('input', debouncedFiltrarLista);
    if (searchUsuarioInput) searchUsuarioInput.addEventListener('input', debouncedFiltrarLista);
    if (searchStatusInput) searchStatusInput.addEventListener('change', debouncedFiltrarLista);

    console.log('=== JAVASCRIPT INICIALIZADO COMPLETAMENTE ===');
}); 