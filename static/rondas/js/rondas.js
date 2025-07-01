document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('rondaForm');
    const formTitle = document.getElementById('formTitle');
    const submitBtn = document.getElementById('submitBtn');
    const rondaIdField = document.getElementById('ronda_id');
    const cancelBtn = document.getElementById('cancelEdit');
    const limparBtn = document.getElementById('limparForm');
    const listContainer = document.getElementById('ronda-list-container');

    if (!form || !listContainer) {
        return;
    }

    const CREATE_URL = form.action;
    const UPDATE_URL_TEMPLATE = listContainer.dataset.updateUrlTemplate;
    const GET_RONDA_URL_TEMPLATE = listContainer.dataset.getUrlTemplate;

    function resetFormToCreateMode() {
        if(form) form.reset();
        if(rondaIdField) rondaIdField.value = '';
        if(formTitle) formTitle.textContent = 'Nova Ronda';
        if(submitBtn) {
            submitBtn.textContent = 'Salvar';
            submitBtn.className = 'btn-primary';
        }
        if(cancelBtn) cancelBtn.style.display = 'none';
        if (form && CREATE_URL) {
            form.action = CREATE_URL;
        }
        if (form) form.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    window.carregarRonda = function(rondaId) {
        const fetchUrl = GET_RONDA_URL_TEMPLATE.replace('0', rondaId);
        formTitle.textContent = 'Carregando...';
        fetch(fetchUrl)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const ronda = data.ronda;
                    if (rondaIdField) rondaIdField.value = ronda.id;
                    const localSelect = document.querySelector('select[name="local"]');
                    if (localSelect && ronda.local_id) localSelect.value = ronda.local_id;
                    const dataHoraInput = document.querySelector('input[name="data_hora"]');
                    if (dataHoraInput && ronda.data_hora) dataHoraInput.value = ronda.data_hora;
                    const statusSelect = document.querySelector('select[name="status"]');
                    if (statusSelect && ronda.status) statusSelect.value = ronda.status;
                    const observacoesTextarea = document.querySelector('textarea[name="observacoes"]');
                    if (observacoesTextarea) observacoesTextarea.value = ronda.observacoes || '';
                    formTitle.textContent = `Editar Ronda: ${ronda.id}`;
                    submitBtn.textContent = 'Atualizar';
                    form.action = UPDATE_URL_TEMPLATE.replace('0', ronda.id);
                    cancelBtn.style.display = 'inline-block';
                    form.scrollIntoView({ behavior: 'smooth', block: 'start' });
                } else {
                    alert(`Erro ao carregar ronda: ${data.error}`);
                    formTitle.textContent = 'Nova Ronda';
                }
            })
            .catch(error => {
                alert(`Erro ao carregar ronda: ${error.message}`);
                formTitle.textContent = 'Nova Ronda';
            });
    }

    if (limparBtn) limparBtn.addEventListener('click', resetFormToCreateMode);
    if (cancelBtn) {
        cancelBtn.addEventListener('click', function() {
            window.location.reload();
        });
    }
    form.addEventListener('submit', function(e) {
        // Permite o submit normal
    });

    // --- BUSCA INSTANTÂNEA ---
    const searchLocalInput = document.getElementById('search-local-input');
    const searchStatusInput = document.getElementById('search-status-input');
    const listResults = document.getElementById('ronda-list-results');

    function debounce(func, wait) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }

    function filtrarLista() {
        const local = searchLocalInput ? searchLocalInput.value : '';
        const status = searchStatusInput ? searchStatusInput.value : '';
        const params = new URLSearchParams({
            search_local: local,
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
    if (searchStatusInput) searchStatusInput.addEventListener('change', debouncedFiltrarLista);
}); 