document.addEventListener('DOMContentLoaded', function() {
    console.log('=== TREINAMENTOS JS CARREGADO ===');
    
    // Elementos do DOM
    const form = document.getElementById('treinamentoForm');
    const formTitle = document.getElementById('formTitle');
    const submitBtn = document.getElementById('submitBtn');
    const treinamentoIdField = document.getElementById('treinamento_id');
    const cancelBtn = document.getElementById('cancelEdit');
    const limparBtn = document.getElementById('limparForm');
    const listContainer = document.getElementById('treinamento-list-container');

    console.log('Elementos encontrados:', {
        form: !!form,
        formTitle: !!formTitle,
        submitBtn: !!submitBtn,
        treinamentoIdField: !!treinamentoIdField,
        listContainer: !!listContainer
    });

    if (!form || !listContainer) {
        console.error('Elementos essenciais não encontrados!');
        return;
    }

    const CREATE_URL = form.action;
    const UPDATE_URL_TEMPLATE = listContainer.dataset.updateUrlTemplate;
    const GET_TREINAMENTO_URL_TEMPLATE = listContainer.dataset.getUrlTemplate;
    
    console.log('URLs configuradas:', {
        CREATE_URL,
        UPDATE_URL_TEMPLATE,
        GET_TREINAMENTO_URL_TEMPLATE
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
        if(treinamentoIdField) treinamentoIdField.value = '';
        if(formTitle) formTitle.textContent = 'Novo Treinamento';
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
     * Função global para carregar os dados de um treinamento no formulário.
     * @param {string} treinamentoId - O ID do treinamento.
     */
    window.carregarTreinamento = function(treinamentoId) {
        console.log(`Carregando treinamento ID: ${treinamentoId}`);
        const fetchUrl = GET_TREINAMENTO_URL_TEMPLATE.replace('0', treinamentoId);

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
                    const treinamento = data.treinamento;
                    
                    // Preenche os campos do formulário
                    if (treinamentoIdField) treinamentoIdField.value = treinamento.id;
                    
                    // Preenche os campos específicos do modelo Treinamento
                    const localSelect = document.querySelector('select[name="local"]');
                    if (localSelect && treinamento.local_id) {
                        localSelect.value = treinamento.local_id;
                    }
                    
                    const usuarioSelect = document.querySelector('select[name="usuario"]');
                    if (usuarioSelect && treinamento.usuario_id) {
                        usuarioSelect.value = treinamento.usuario_id;
                    }
                    
                    const dataHoraInput = document.querySelector('input[name="data_hora"]');
                    if (dataHoraInput && treinamento.data_hora) {
                        dataHoraInput.value = treinamento.data_hora;
                    }
                    
                    const statusSelect = document.querySelector('select[name="status"]');
                    if (statusSelect && treinamento.status) {
                        statusSelect.value = treinamento.status;
                    }

                    // Atualiza a UI para o modo de edição
                    formTitle.textContent = `Editar Treinamento: ${treinamento.id}`;
                    submitBtn.textContent = 'Atualizar';
                    form.action = UPDATE_URL_TEMPLATE.replace('0', treinamento.id);
                    cancelBtn.style.display = 'inline-block';
                    form.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    
                    console.log('Treinamento carregado com sucesso:', treinamento);
                } else {
                    console.error('Erro ao carregar treinamento:', data.error);
                    alert(`Erro ao carregar treinamento: ${data.error}`);
                    formTitle.textContent = 'Novo Treinamento';
                }
            })
            .catch(error => {
                console.error('Erro na requisição:', error);
                alert(`Erro ao carregar treinamento: ${error.message}`);
                formTitle.textContent = 'Novo Treinamento';
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
    const listResults = document.getElementById('treinamento-list-results');

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

    console.log('=== TREINAMENTOS JS INICIALIZADO COMPLETAMENTE ===');
}); 