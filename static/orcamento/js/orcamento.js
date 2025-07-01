document.addEventListener('DOMContentLoaded', function() {
    console.log('=== ORÇAMENTO JS CARREGADO ===');

    // Elementos do DOM
    const form = document.getElementById('orcamentoForm');
    const formTitle = document.getElementById('form-title');
    const submitBtn = document.getElementById('btn-salvar');
    const orcamentoIdField = document.getElementById('orcamento_id');
    const cancelBtn = document.getElementById('cancelEdit');
    const limparBtn = document.getElementById('btn-novo');
    const listContainer = document.getElementById('orcamento-list-container');
    const localSelect = document.getElementById('id_nome_local');
    const usuarioSelect = document.getElementById('id_nome_usuarios');

    if (!form || !listContainer || !localSelect || !usuarioSelect) {
        console.error('Elementos essenciais do formulário Orçamento não encontrados!');
        return;
    }

    const CREATE_URL = form.action;
    const UPDATE_URL_TEMPLATE = listContainer.dataset.updateUrlTemplate;

    // --- FUNÇÕES ---

    /**
     * Reseta o formulário para o modo de criação.
     */
    function resetFormToCreateMode() {
        console.log('Resetando formulário Orçamento...');
        form.reset();
        orcamentoIdField.value = '';
        formTitle.textContent = 'Novo Orçamento';
        submitBtn.textContent = 'Salvar';
        submitBtn.className = 'px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700';
        cancelBtn.style.display = 'none';
        form.action = CREATE_URL;
        form.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
        // Remover seleção de todos os itens
        document.querySelectorAll('.orcamento-item').forEach(item => {
            item.classList.remove('selected');
        });
    }

    /**
     * Função global para carregar os dados de um orçamento no formulário.
     * @param {string} orcamentoId - O ID do orçamento.
     */
    window.carregarOrcamento = function(orcamentoId) {
        console.log(`Carregando Orçamento ID: ${orcamentoId}`);
        const GET_ORCAMENTO_URL_TEMPLATE = listContainer.dataset.getUrlTemplate;
        const fetchUrl = GET_ORCAMENTO_URL_TEMPLATE.replace('0', orcamentoId);

        formTitle.textContent = 'Carregando...';
        
        // Remover seleção anterior
        document.querySelectorAll('.orcamento-item').forEach(item => {
            item.classList.remove('selected');
        });
        
        // Adicionar seleção ao item clicado
        const itemClicado = document.querySelector(`[data-orcamento-id="${orcamentoId}"]`);
        if (itemClicado) {
            itemClicado.classList.add('selected');
        }
        
        fetch(fetchUrl)
            .then(response => response.json())
            .then(data => {
                console.log('Dados recebidos:', data);
                
                if (data.success) {
                    const orcamento = data.orcamento;
                    
                    // Preenche o formulário com os dados do orçamento
                    orcamentoIdField.value = orcamento.id;
                    localSelect.value = orcamento.nome_local;
                    usuarioSelect.value = orcamento.nome_usuarios;
                    document.getElementById('id_data_acionamento').value = orcamento.data_acionamento;
                    document.getElementById('id_data_chegada').value = orcamento.data_chegada;
                    document.getElementById('id_sla_resposta').value = orcamento.sla_resposta;

                    // Atualiza a UI para o modo de edição
                    formTitle.textContent = 'Editar Orçamento';
                    submitBtn.textContent = 'Atualizar';
                    form.action = UPDATE_URL_TEMPLATE;
                    cancelBtn.style.display = 'inline-block';
                    form.scrollIntoView({ behavior: 'smooth', block: 'start' });
                } else {
                    alert(`Erro ao carregar orçamento: ${data.error}`);
                    formTitle.textContent = 'Novo Orçamento';
                }
            })
            .catch(error => {
                console.error('Erro na requisição:', error);
                alert(`Erro ao carregar orçamento: ${error.message}`);
                formTitle.textContent = 'Novo Orçamento';
            });
    }

    /**
     * Realiza a busca por AJAX.
     */
    const performSearch = () => {
        const searchQuery = document.querySelector('input[name="q"]').value;
        const resultsContainer = document.getElementById('orcamento-list-results');
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
        console.log('Formulário Orçamento submetido.');
        // Permite o envio padrão do formulário
    });

    // Adicionar evento de busca
    const searchInput = document.querySelector('input[name="q"]');
    if (searchInput) {
        searchInput.addEventListener('input', debouncedSearch);
    }

    console.log('=== ORÇAMENTO JS INICIALIZADO ===');
}); 