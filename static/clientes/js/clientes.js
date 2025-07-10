
document.addEventListener('DOMContentLoaded', function() {
    console.log('=== CLIENTES JS CARREGADO ===');

    // Elementos do DOM
    const form = document.getElementById('clienteForm');
    const formTitle = document.getElementById('formTitle');
    const submitBtn = document.getElementById('submitBtn');
    const clienteIdField = document.getElementById('cliente_id');
    const cancelBtn = document.getElementById('cancelEdit');
    const listContainer = document.getElementById('client-list-container');
    const nomeInput = document.getElementById('nome');
    const prontaRespostaInput = document.getElementById('pronta_resposta');
    const telefoneInput = document.getElementById('telefone');
    const quantidadeInput = document.getElementById('quantidade');
    const produtoSelect = document.getElementById('id_produto') || document.getElementById('produto');

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
        const GET_CLIENT_URL_TEMPLATE = listContainer.dataset.getUrlTemplate;
        const fetchUrl = GET_CLIENT_URL_TEMPLATE.replace('0', clienteId);
        formTitle.textContent = 'Carregando...';
        document.querySelectorAll('.cliente-item').forEach(item => {
            item.classList.remove('selected');
        });
        const itemClicado = document.querySelector(`[data-cliente-id="${clienteId}"]`);
        if (itemClicado) {
            itemClicado.classList.add('selected');
        }
        fetch(fetchUrl)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const cliente = data.cliente;
                    clienteIdField.value = cliente.id;
                    nomeInput.value = cliente.nome || '';
                    prontaRespostaInput.value = cliente.pronta_resposta || '';
                    telefoneInput.value = cliente.telefone || '';

                    // Limpa todas as linhas de produtos, exceto a primeira
                    const produtosContainer = document.getElementById('produtos-container');
                    let rows = produtosContainer.querySelectorAll('.produto-row');
                    rows.forEach((row, idx) => { if (idx > 0) row.remove(); });

                    // Preenche os produtos do cliente
                    if (cliente.produtos && cliente.produtos.length > 0) {
                        cliente.produtos.forEach((prod, idx) => {
                            let row;
                            if (idx === 0) {
                                row = produtosContainer.querySelector('.produto-row');
                            } else {
                                row = produtosContainer.querySelector('.produto-row').cloneNode(true);
                                produtosContainer.appendChild(row);
                            }
                            row.querySelector('.produto-select').value = prod.produto_id;
                            row.querySelector('.quantidade-input').value = prod.quantidade;
                            // Exibe botão remover nas linhas extras
                            if (idx > 0) {
                                row.querySelector('.remover-produto').style.display = 'inline-block';
                                row.querySelector('.remover-produto').onclick = function() {
                                    row.remove();
                                };
                            } else {
                                row.querySelector('.remover-produto').style.display = 'none';
                            }
                        });
                    } else {
                        // Se não houver produtos, limpa a primeira linha
                        let row = produtosContainer.querySelector('.produto-row');
                        row.querySelector('.produto-select').selectedIndex = 0;
                        row.querySelector('.quantidade-input').value = 1;
                        row.querySelector('.remover-produto').style.display = 'none';
                    }

                    formTitle.textContent = `Editar Local: ${cliente.nome}`;
                    submitBtn.textContent = 'Atualizar';
                    // Remover qualquer linha como: form.action = UPDATE_URL_TEMPLATE.replace('0', cliente.id);
                    // O formulário deve sempre enviar para a URL padrão definida no template.
                    cancelBtn.style.display = 'inline-block';
                    form.scrollIntoView({ behavior: 'smooth', block: 'start' });
                } else {
                    alert(`Erro ao carregar cliente: ${data.error}`);
                    formTitle.textContent = 'Novo Local';
                }
            })
            .catch(error => {
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

    // --- PRODUTOS DINÂMICOS ---
    const produtosContainer = document.getElementById('produtos-container');
    const adicionarProdutoBtn = document.getElementById('adicionar-produto');

    if (adicionarProdutoBtn && produtosContainer) {
        adicionarProdutoBtn.addEventListener('click', function() {
            const firstRow = produtosContainer.querySelector('.produto-row');
            const newRow = firstRow.cloneNode(true);
            // Limpa valores do novo campo
            newRow.querySelector('.produto-select').selectedIndex = 0;
            newRow.querySelector('.quantidade-input').value = 1;
            newRow.querySelector('.remover-produto').style.display = 'inline-block';
            // Adiciona evento de remover
            newRow.querySelector('.remover-produto').onclick = function() {
                newRow.remove();
            };
            produtosContainer.appendChild(newRow);
        });
        // Ativa botão remover no clone inicial se houver mais de um
        produtosContainer.querySelectorAll('.remover-produto').forEach(btn => {
            btn.onclick = function() {
                btn.closest('.produto-row').remove();
            };
        });
    }

    // --- EVENT LISTENERS ---

    // Tornar cada item da lista clicável
    document.querySelectorAll('.cliente-item').forEach(function(item) {
        item.addEventListener('click', function() {
            const clienteId = this.getAttribute('data-cliente-id');
            window.carregarCliente(clienteId);
        });
    });

    // Botão de cancelar edição
    if (cancelBtn) {
        cancelBtn.addEventListener('click', function(e) {
            e.preventDefault();
            resetFormToCreateMode();
        });
    }

    // Resetar formulário ao submeter (opcional)
    form.addEventListener('submit', function(e) {
        submitBtn.textContent = 'Salvando...';
        submitBtn.disabled = true;
        // Permite o envio padrão do formulário
        setTimeout(function() {
            // Após o submit, atualiza a listagem via AJAX
            fetch('/clientes/lista_clientes_partial/')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('client-list-results').innerHTML = data.html;
                    // Reaplica eventos de clique nos novos itens
                    document.querySelectorAll('.cliente-item').forEach(function(item) {
                        item.addEventListener('click', function() {
                            const clienteId = this.getAttribute('data-cliente-id');
                            window.carregarCliente(clienteId);
                        });
                    });
                });
        }, 500); // Pequeno delay para garantir que o backend já salvou
    });

    // Inicialização
    resetFormToCreateMode();

    console.log('=== CLIENTES JS INICIALIZADO ===');
}); 