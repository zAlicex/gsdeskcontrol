document.addEventListener('DOMContentLoaded', function() {
    console.log('=== ORPECAS JS CARREGADO ===');

    // --- ELEMENTOS DO DOM ---
    const form = document.getElementById('orpecasForm');
    if (!form) return;

    const formTitle = document.getElementById('formTitle');
    const submitBtn = document.getElementById('submitBtn');
    const orpecasIdField = document.getElementById('orpecas_id');
    const cancelBtn = document.getElementById('cancelEdit');
    const limparBtn = document.getElementById('limparForm');
    const listContainer = document.getElementById('orpecas-list-container');
    
    const CREATE_URL = form.action;
    const UPDATE_URL_TEMPLATE = listContainer.dataset.updateUrlTemplate;
    const GET_ORPECAS_URL_TEMPLATE = listContainer.dataset.getUrlTemplate;

    // --- FUNÇÕES ---

    /**
     * Reseta o formulário para o estado inicial.
     */
    function resetFormToCreateMode() {
        form.reset();
        orpecasIdField.value = '';
        formTitle.textContent = 'Novo Orpecas';
        submitBtn.textContent = 'Salvar';
        cancelBtn.style.display = 'none';
        form.action = CREATE_URL;
        form.scrollIntoView({ behavior: 'smooth' });
        
        // Limpar preview da imagem
        const preview = document.getElementById('imagem-preview');
        if (preview) {
            preview.classList.add('hidden');
        }
        
        // Remover seleção de todos os itens
        document.querySelectorAll('.orpecas-item').forEach(item => {
            item.classList.remove('selected');
        });
    }

    /**
     * Carrega um orpecas existente no formulário.
     * @param {string} orpecasId - O ID do orpecas.
     */
    window.carregarOrpecas = function(orpecasId) {
        console.log(`Carregando Orpecas ID: ${orpecasId}`);
        const fetchUrl = GET_ORPECAS_URL_TEMPLATE.replace('0', orpecasId);

        formTitle.textContent = 'Carregando...';
        
        // Remover seleção anterior
        document.querySelectorAll('.orpecas-item').forEach(item => {
            item.classList.remove('selected');
        });
        
        // Adicionar seleção ao item clicado
        const itemClicado = document.querySelector(`[data-orpecas-id="${orpecasId}"]`);
        if (itemClicado) {
            itemClicado.classList.add('selected');
        }
        
        fetch(fetchUrl)
            .then(response => response.json())
            .then(data => {
                console.log('Dados recebidos:', data);
                
                if (data.success) {
                    const orpecas = data.orpecas;
                    
                    // Preenche o formulário com os dados do orpecas
                    orpecasIdField.value = orpecas.id;
                    
                    // Preenche os campos do formulário
                    const localField = document.getElementById('id_local');
                    const diagnosticoField = document.getElementById('id_diagnostico');
                    const botaoPanicoField = document.getElementById('id_botao_panico');
                    const sensorField = document.getElementById('id_sensor');
                    
                    if (localField) localField.value = orpecas.local;
                    if (diagnosticoField) diagnosticoField.value = orpecas.diagnostico;
                    if (botaoPanicoField) botaoPanicoField.value = orpecas.botao_panico;
                    if (sensorField) sensorField.value = orpecas.sensor;

                    // Processar imagem se existir
                    const preview = document.getElementById('imagem-preview');
                    const previewImg = document.getElementById('preview-img');
                    if (orpecas.imagem_url && preview && previewImg) {
                        previewImg.src = orpecas.imagem_url;
                        preview.classList.remove('hidden');
                    } else if (preview) {
                        preview.classList.add('hidden');
                    }

                    // Atualiza a UI para modo de edição
                    formTitle.textContent = `Editar Orpecas: ${orpecas.id}`;
                    submitBtn.textContent = 'Atualizar';
                    form.action = UPDATE_URL_TEMPLATE.replace('0', orpecas.id);
                    cancelBtn.style.display = 'inline-block';
                    form.scrollIntoView({ behavior: 'smooth' });
                } else {
                    alert(`Erro ao carregar orpecas: ${data.error}`);
                    formTitle.textContent = 'Novo Orpecas';
                }
            })
            .catch(error => {
                console.error('Erro na requisição:', error);
                alert(`Erro ao carregar orpecas: ${error.message}`);
                formTitle.textContent = 'Novo Orpecas';
            });
    }

    /**
     * Realiza a busca por AJAX.
     */
    const performSearch = () => {
        const searchLocal = document.getElementById('search-local-input')?.value || '';
        const searchDiagnostico = document.getElementById('search-diagnostico-input')?.value || '';
        const resultsContainer = document.getElementById('orpecas-list-results');
        const searchUrl = `${window.location.pathname}?search_local=${encodeURIComponent(searchLocal)}&search_diagnostico=${encodeURIComponent(searchDiagnostico)}`;

        resultsContainer.innerHTML = '<div class="p-4 text-center">Buscando...</div>';

        fetch(searchUrl, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
            .then(response => response.json())
            .then(data => {
                resultsContainer.innerHTML = data.html;
            })
            .catch(error => {
                console.error('Erro na busca AJAX:', error);
                resultsContainer.innerHTML = '<div class="p-4 text-center text-red-500">Erro ao buscar.</div>';
            });
    };
    
    const debounce = (func, delay) => {
        let timeoutId;
        return (...args) => {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => func.apply(this, args), delay);
        };
    };
    const debouncedSearch = debounce(performSearch, 300);

    // --- EVENT LISTENERS ---
    if (limparBtn) limparBtn.addEventListener('click', resetFormToCreateMode);
    if (cancelBtn) cancelBtn.addEventListener('click', () => window.location.reload());
    
    form.addEventListener('submit', function() {
        console.log('Formulário Orpecas submetido.');
        // Permite o envio padrão do formulário
    });

    // Adicionar eventos de busca
    const searchLocalInput = document.getElementById('search-local-input');
    const searchDiagnosticoInput = document.getElementById('search-diagnostico-input');
    
    if (searchLocalInput) searchLocalInput.addEventListener('input', debouncedSearch);
    if (searchDiagnosticoInput) searchDiagnosticoInput.addEventListener('input', debouncedSearch);

    console.log('=== ORPECAS JS INICIALIZADO ===');
}); 