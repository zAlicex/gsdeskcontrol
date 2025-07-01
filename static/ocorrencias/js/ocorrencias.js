// Ocorrências JavaScript
let ocorrenciaIdParaExcluir = null;

document.addEventListener('DOMContentLoaded', function() {
    console.log('=== OCORRÊNCIAS JS CARREGADO ===');

    // Elementos do DOM
    const form = document.getElementById('ocorrenciaForm');
    const formTitle = document.getElementById('formTitle');
    const submitBtn = document.getElementById('submitBtn');
    const ocorrenciaIdField = document.getElementById('ocorrencia_id');
    const cancelBtn = document.getElementById('cancelEdit');
    const listContainer = document.getElementById('ocorrencia-list-container');
    const localSelect = document.getElementById('local');

    if (!form || !listContainer || !localSelect) {
        console.error('Elementos essenciais do formulário Ocorrências não encontrados!');
        return;
    }

    const CREATE_URL = form.action;
    const UPDATE_URL_TEMPLATE = listContainer.dataset.updateUrlTemplate;

    // --- FUNÇÕES ---

    /**
     * Reseta o formulário para o modo de criação.
     */
    function resetFormToCreateMode() {
        console.log('Resetando formulário Ocorrências...');
        form.reset();
        ocorrenciaIdField.value = '';
        formTitle.textContent = 'Nova Ocorrência';
        submitBtn.textContent = 'Salvar';
        submitBtn.className = 'btn-primary';
        cancelBtn.style.display = 'none';
        form.action = CREATE_URL;
        form.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    /**
     * Função global para carregar os dados de uma ocorrência no formulário.
     * @param {string} ocorrenciaId - O ID da ocorrência.
     */
    window.carregarOcorrencia = function(ocorrenciaId) {
        console.log(`Carregando Ocorrência ID: ${ocorrenciaId}`);
        const GET_OCORRENCIA_URL_TEMPLATE = listContainer.dataset.getUrlTemplate;
        const fetchUrl = GET_OCORRENCIA_URL_TEMPLATE.replace('0', ocorrenciaId);

        formTitle.textContent = 'Carregando...';
        
        fetch(fetchUrl)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const ocorrencia = data.ocorrencia;
                    // Preenche os campos reais do modelo
                    if (localSelect) localSelect.value = ocorrencia.local;
                    document.getElementById('data_hora').value = ocorrencia.data_hora || '';
                    document.getElementById('status').value = ocorrencia.status || '';
                    document.getElementById('observacoes').value = ocorrencia.observacoes || '';

                    // Atualiza a UI para o modo de edição
                    ocorrenciaIdField.value = ocorrencia.id;
                    formTitle.textContent = `Editar Ocorrência: ${ocorrencia.local_nome || 'Local'}`;
                    submitBtn.textContent = 'Atualizar';
                    form.action = UPDATE_URL_TEMPLATE.replace('0', ocorrencia.id);
                    cancelBtn.style.display = 'inline-block';
                    form.scrollIntoView({ behavior: 'smooth', block: 'start' });
                } else {
                    alert(`Erro ao carregar ocorrência: ${data.error}`);
                    formTitle.textContent = 'Nova Ocorrência';
                }
            })
            .catch(error => {
                console.error('Erro na requisição:', error);
                alert(`Erro ao carregar ocorrência: ${error.message}`);
                formTitle.textContent = 'Nova Ocorrência';
            });
    }

    /**
     * Realiza a busca por AJAX.
     */
    const performSearch = () => {
        const searchLocal = document.getElementById('search-local-input').value;
        const searchStatus = document.getElementById('search-status-input').value;
        const resultsContainer = document.getElementById('ocorrencia-list-results');
        const searchUrl = `${window.location.pathname}?search_local=${encodeURIComponent(searchLocal)}&search_status=${encodeURIComponent(searchStatus)}`;

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

    if (cancelBtn) cancelBtn.addEventListener('click', () => window.location.reload());

    form.addEventListener('submit', function() {
        console.log('Formulário Ocorrências submetido.');
        // Permite o envio padrão do formulário
    });

    // Event listeners para busca
    const searchLocalInput = document.getElementById('search-local-input');
    const searchStatusInput = document.getElementById('search-status-input');
    
    if (searchLocalInput) {
        searchLocalInput.addEventListener('input', debouncedSearch);
    }
    if (searchStatusInput) {
        searchStatusInput.addEventListener('change', debouncedSearch);
    }

    console.log('=== OCORRÊNCIAS JS INICIALIZADO ===');
});

function salvarOcorrencia() {
    const form = document.getElementById('ocorrenciaForm');
    const formData = new FormData(form);
    
    fetch('/ocorrencias/salvar/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Ocorrência salva com sucesso!');
            limparFormulario();
            buscarOcorrencias(); // Atualizar lista
        } else {
            alert('Erro ao salvar: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao salvar ocorrência');
    });
}

function excluirOcorrencia() {
    const ocorrenciaId = document.getElementById('ocorrencia_id').value;
    if (!ocorrenciaId) {
        alert('Nenhuma ocorrência selecionada para exclusão');
        return;
    }
    
    ocorrenciaIdParaExcluir = ocorrenciaId;
    document.getElementById('confirmModal').classList.remove('hidden');
}

function confirmarExclusao() {
    if (!ocorrenciaIdParaExcluir) return;
    
    fetch(`/ocorrencias/excluir/${ocorrenciaIdParaExcluir}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Ocorrência excluída com sucesso!');
            limparFormulario();
            buscarOcorrencias();
            fecharModal();
        } else {
            alert('Erro ao excluir: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao excluir ocorrência');
    });
}

function fecharModal() {
    document.getElementById('confirmModal').classList.add('hidden');
    ocorrenciaIdParaExcluir = null;
}

function limparFormulario() {
    document.getElementById('ocorrenciaForm').reset();
    document.getElementById('ocorrencia_id').value = '';
    document.getElementById('btnExcluir').style.display = 'none';
    
    // Remover seleção dos itens
    document.querySelectorAll('.ocorrencia-item').forEach(item => {
        item.classList.remove('selected');
    });
    
    // Definir data/hora atual
    const now = new Date();
    const localDateTime = new Date(now.getTime() - now.getTimezoneOffset() * 60000)
        .toISOString().slice(0, 16);
    document.getElementById('id_data_hora').value = localDateTime;
}

function buscarOcorrencias() {
    const searchTerm = document.getElementById('searchInput').value;
    
    fetch('/ocorrencias/buscar/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: `search=${encodeURIComponent(searchTerm)}`
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById('listaOcorrencias').innerHTML = html;
    })
    .catch(error => {
        console.error('Erro na busca:', error);
    });
}

// Event listeners para busca
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                buscarOcorrencias();
            }
        });
    }
}); 