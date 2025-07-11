
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
        
        // Limpar containers dinâmicos
        limparProntasRespostas();
        limparTelefones();
    }

    /**
     * Limpa o container de prontas respostas
     */
    function limparProntasRespostas() {
        const container = document.getElementById('prontas-respostas-container');
        if (container) {
            container.innerHTML = '';
        }
    }

    /**
     * Limpa o container de telefones
     */
    function limparTelefones() {
        const container = document.getElementById('telefones-container');
        if (container) {
            container.innerHTML = '';
        }
    }

    /**
     * Adiciona uma nova pronta resposta dinamicamente
     */
    function adicionarProntaResposta() {
        const clienteId = clienteIdField.value;
        if (!clienteId) {
            alert('Selecione um cliente primeiro');
            return;
        }

        const prontaResposta = prompt('Digite a pronta resposta:');
        if (!prontaResposta) return;

        const formData = new FormData();
        formData.append('pronta_resposta', prontaResposta);

        fetch(`/locais/cliente/${clienteId}/adicionar-pronta-resposta/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                carregarProntasRespostas(clienteId);
            } else {
                alert('Erro ao adicionar pronta resposta: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao adicionar pronta resposta');
        });
    }

    /**
     * Remove uma pronta resposta
     */
    function removerProntaResposta(prontaRespostaId) {
        const clienteId = clienteIdField.value;
        if (!confirm('Tem certeza que deseja remover esta pronta resposta?')) return;

        fetch(`/locais/cliente/${clienteId}/remover-pronta-resposta/${prontaRespostaId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                carregarProntasRespostas(clienteId);
            } else {
                alert('Erro ao remover pronta resposta: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao remover pronta resposta');
        });
    }

    /**
     * Carrega as prontas respostas do cliente
     */
    function carregarProntasRespostas(clienteId) {
        fetch(`/locais/get_cliente/${clienteId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const container = document.getElementById('prontas-respostas-container');
                if (container) {
                    container.innerHTML = '';
                    data.cliente.prontas_respostas.forEach(pr => {
                        const item = document.createElement('div');
                        item.className = 'flex items-center justify-between p-2 bg-gray-50 rounded mb-2';
                        item.innerHTML = `
                            <span>${pr.pronta_resposta}</span>
                            <button type="button" onclick="removerProntaResposta(${pr.id})" 
                                    class="text-red-600 hover:text-red-800">
                                <i class="fas fa-trash"></i>
                            </button>
                        `;
                        container.appendChild(item);
                    });
                }
            }
        })
        .catch(error => {
            console.error('Erro ao carregar prontas respostas:', error);
        });
    }

    /**
     * Adiciona um novo telefone dinamicamente
     */
    function adicionarTelefone() {
        const clienteId = clienteIdField.value;
        if (!clienteId) {
            alert('Selecione um cliente primeiro');
            return;
        }

        const telefone = prompt('Digite o telefone:');
        if (!telefone) return;

        const tipo = prompt('Digite o tipo (ex: Celular, Fixo) - opcional:') || '';

        const formData = new FormData();
        formData.append('telefone', telefone);
        formData.append('tipo', tipo);

        fetch(`/locais/cliente/${clienteId}/adicionar-telefone/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                carregarTelefones(clienteId);
            } else {
                alert('Erro ao adicionar telefone: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao adicionar telefone');
        });
    }

    /**
     * Remove um telefone
     */
    function removerTelefone(telefoneId) {
        const clienteId = clienteIdField.value;
        if (!confirm('Tem certeza que deseja remover este telefone?')) return;

        fetch(`/locais/cliente/${clienteId}/remover-telefone/${telefoneId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                carregarTelefones(clienteId);
            } else {
                alert('Erro ao remover telefone: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao remover telefone');
        });
    }

    /**
     * Carrega os telefones do cliente
     */
    function carregarTelefones(clienteId) {
        fetch(`/locais/get_cliente/${clienteId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const container = document.getElementById('telefones-container');
                if (container) {
                    container.innerHTML = '';
                    data.cliente.telefones.forEach(tel => {
                        const item = document.createElement('div');
                        item.className = 'flex items-center justify-between p-2 bg-gray-50 rounded mb-2';
                        item.innerHTML = `
                            <div>
                                <span class="font-medium">${tel.telefone}</span>
                                ${tel.tipo ? `<span class="text-sm text-gray-500 ml-2">(${tel.tipo})</span>` : ''}
                            </div>
                            <button type="button" onclick="removerTelefone(${tel.id})" 
                                    class="text-red-600 hover:text-red-800">
                                <i class="fas fa-trash"></i>
                            </button>
                        `;
                        container.appendChild(item);
                    });
                }
            }
        })
        .catch(error => {
            console.error('Erro ao carregar telefones:', error);
        });
    }

    /**
     * Função para obter o token CSRF
     */
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
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

                    // Carregar prontas respostas e telefones dinâmicos
                    carregarProntasRespostas(cliente.id);
                    carregarTelefones(cliente.id);
                    carregarProntasTelefones(cliente.id);

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

    // Expor funções globalmente
    window.adicionarProntaResposta = adicionarProntaResposta;
    window.removerProntaResposta = removerProntaResposta;
    window.adicionarTelefone = adicionarTelefone;
    window.removerTelefone = removerTelefone;
    window.abrirAdicionarProntaTelefone = abrirAdicionarProntaTelefone;

    // --- ARRAYS LOCAIS PARA ITENS DINÂMICOS ---
    let prontasRespostasTemp = [];
    let telefonesTemp = [];

    // Renderiza os itens dinâmicos na tela
    function renderProntasTelefones() {
        const container = document.getElementById('prontas-telefones-container');
        container.innerHTML = '';
        // Prontas Respostas
        if (prontasRespostasTemp.length > 0) {
            const prontasDiv = document.createElement('div');
            prontasDiv.className = 'mb-3';
            prontasDiv.innerHTML = '<div class="text-sm font-medium text-gray-700 mb-2">Prontas Respostas:</div>';
            prontasRespostasTemp.forEach((pr, idx) => {
                const item = document.createElement('div');
                item.className = 'flex items-center justify-between p-2 bg-white rounded border mb-1';
                item.innerHTML = `
                    <span class="text-sm">${pr}</span>
                    <button type="button" class="text-red-600 hover:text-red-800 text-sm" onclick="window.removerProntaRespostaTemp(${idx})">
                        <i class="fas fa-trash"></i>
                    </button>
                `;
                prontasDiv.appendChild(item);
            });
            container.appendChild(prontasDiv);
        }
        // Telefones
        if (telefonesTemp.length > 0) {
            const telefonesDiv = document.createElement('div');
            telefonesDiv.className = 'mb-3';
            telefonesDiv.innerHTML = '<div class="text-sm font-medium text-gray-700 mb-2">Telefones:</div>';
            telefonesTemp.forEach((tel, idx) => {
                const item = document.createElement('div');
                item.className = 'flex items-center justify-between p-2 bg-white rounded border mb-1';
                item.innerHTML = `
                    <div class="text-sm">
                        <span class="font-medium">${tel.telefone}</span>
                        ${tel.tipo ? `<span class="text-gray-500 ml-2">(${tel.tipo})</span>` : ''}
                    </div>
                    <button type="button" class="text-red-600 hover:text-red-800 text-sm" onclick="window.removerTelefoneTemp(${idx})">
                        <i class="fas fa-trash"></i>
                    </button>
                `;
                telefonesDiv.appendChild(item);
            });
            container.appendChild(telefonesDiv);
        }
        // Se não há itens, mostrar mensagem
        if (prontasRespostasTemp.length === 0 && telefonesTemp.length === 0) {
            const emptyDiv = document.createElement('div');
            emptyDiv.className = 'text-gray-500 text-sm italic';
            emptyDiv.textContent = 'Nenhum item adicional cadastrado';
            container.appendChild(emptyDiv);
        }
    }

    // Funções globais para remover itens
    window.removerProntaRespostaTemp = function(idx) {
        prontasRespostasTemp.splice(idx, 1);
        renderProntasTelefones();
    };
    window.removerTelefoneTemp = function(idx) {
        telefonesTemp.splice(idx, 1);
        renderProntasTelefones();
    };

    // Novo abrirAdicionarProntaTelefone para modo criação
    function abrirAdicionarProntaTelefone() {
        // Adiciona uma nova linha de input para pronta resposta e telefone
        const container = document.getElementById('prontas-telefones-container');
        // Cria linha de input
        const linhaDiv = document.createElement('div');
        linhaDiv.className = 'flex gap-2 items-center mb-2 pronta-telefone-linha';
        linhaDiv.innerHTML = `
            <input type="text" placeholder="Pronta Resposta" class="form-control flex-1" autocomplete="off">
            <input type="text" placeholder="Telefone" class="form-control flex-1" autocomplete="off">
            <input type="text" placeholder="Tipo (opcional)" class="form-control" style="width: 120px;">
            <button type="button" class="text-red-600 hover:text-red-800 text-sm btn-remover-linha"><i class="fas fa-trash"></i></button>
        `;
        container.appendChild(linhaDiv);
        const [inputPronta, inputTel, inputTipo, btnRemover] = linhaDiv.querySelectorAll('input,button');
        inputPronta.focus();
        // Função para salvar a linha
        function salvarLinha() {
            const pronta = inputPronta.value.trim();
            const tel = inputTel.value.trim();
            const tipo = inputTipo.value.trim();
            let added = false;
            if (pronta) {
                prontasRespostasTemp.push(pronta);
                added = true;
            }
            if (tel) {
                telefonesTemp.push({ telefone: tel, tipo: tipo });
                added = true;
            }
            if (added) {
                renderProntasTelefones();
                linhaDiv.remove();
            }
        }
        // Enter para salvar
        inputPronta.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') { e.preventDefault(); salvarLinha(); }
        });
        inputTel.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') { e.preventDefault(); salvarLinha(); }
        });
        inputTipo.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') { e.preventDefault(); salvarLinha(); }
        });
        // Blur para salvar
        inputPronta.addEventListener('blur', function() { if (this.value.trim()) salvarLinha(); });
        inputTel.addEventListener('blur', function() { if (this.value.trim()) salvarLinha(); });
        // Remover linha
        btnRemover.onclick = function() { linhaDiv.remove(); };
    }
    window.abrirAdicionarProntaTelefone = abrirAdicionarProntaTelefone;

    function carregarProntasTelefones(clienteId) {
        fetch(`/locais/get_cliente/${clienteId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const container = document.getElementById('prontas-telefones-container');
                
                // Limpar apenas os itens existentes, mantendo o formulário se estiver aberto
                const formDiv = document.getElementById('form-pronta-telefone');
                container.innerHTML = '';
                if (formDiv) {
                    container.appendChild(formDiv);
                }

                // Adicionar prontas respostas
                if (data.cliente.prontas_respostas && data.cliente.prontas_respostas.length > 0) {
                    const prontasDiv = document.createElement('div');
                    prontasDiv.className = 'mb-3';
                    prontasDiv.innerHTML = '<div class="text-sm font-medium text-gray-700 mb-2">Prontas Respostas:</div>';
                    
                    data.cliente.prontas_respostas.forEach(pr => {
                        const item = document.createElement('div');
                        item.className = 'flex items-center justify-between p-2 bg-white rounded border mb-1';
                        item.innerHTML = `
                            <span class="text-sm">${pr.pronta_resposta}</span>
                            <button type="button" onclick="removerProntaResposta(${pr.id})" 
                                    class="text-red-600 hover:text-red-800 text-sm">
                                <i class="fas fa-trash"></i>
                            </button>
                        `;
                        prontasDiv.appendChild(item);
                    });
                    container.appendChild(prontasDiv);
                }

                // Adicionar telefones
                if (data.cliente.telefones && data.cliente.telefones.length > 0) {
                    const telefonesDiv = document.createElement('div');
                    telefonesDiv.className = 'mb-3';
                    telefonesDiv.innerHTML = '<div class="text-sm font-medium text-gray-700 mb-2">Telefones:</div>';
                    
                    data.cliente.telefones.forEach(tel => {
                        const item = document.createElement('div');
                        item.className = 'flex items-center justify-between p-2 bg-white rounded border mb-1';
                        item.innerHTML = `
                            <div class="text-sm">
                                <span class="font-medium">${tel.telefone}</span>
                                ${tel.tipo ? `<span class="text-gray-500 ml-2">(${tel.tipo})</span>` : ''}
                            </div>
                            <button type="button" onclick="removerTelefone(${tel.id})" 
                                    class="text-red-600 hover:text-red-800 text-sm">
                                <i class="fas fa-trash"></i>
                            </button>
                        `;
                        telefonesDiv.appendChild(item);
                    });
                    container.appendChild(telefonesDiv);
                }

                // Se não há itens, mostrar mensagem
                if ((!data.cliente.prontas_respostas || data.cliente.prontas_respostas.length === 0) && 
                    (!data.cliente.telefones || data.cliente.telefones.length === 0)) {
                    const emptyDiv = document.createElement('div');
                    emptyDiv.className = 'text-gray-500 text-sm italic';
                    emptyDiv.textContent = 'Nenhum item adicional cadastrado';
                    container.appendChild(emptyDiv);
                }
            }
        })
        .catch(error => {
            console.error('Erro ao carregar prontas respostas e telefones:', error);
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

    // Resetar arrays e renderização ao criar novo
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
        
        // Limpar containers dinâmicos
        limparProntasRespostas();
        limparTelefones();
        prontasRespostasTemp = [];
        telefonesTemp = [];
        renderProntasTelefones();
    }

    // Inicialização
    resetFormToCreateMode();

    // Adicionar validação no submit
    form.addEventListener('submit', function(e) {
        // Remove campos antigos
        form.querySelectorAll('.pronta-resposta-hidden, .telefone-hidden').forEach(el => el.remove());
        // Adiciona prontas respostas
        prontasRespostasTemp.forEach((pr, idx) => {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = `prontas_respostas_json`;
            input.value = pr;
            input.className = 'pronta-resposta-hidden';
            form.appendChild(input);
        });
        // Adiciona telefones
        telefonesTemp.forEach((tel, idx) => {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = `telefones_json`;
            input.value = JSON.stringify(tel);
            input.className = 'telefone-hidden';
            form.appendChild(input);
        });
        // Validação: pelo menos 5 prontas respostas
        if (prontasRespostasTemp.length < 5) {
            e.preventDefault();
            alert('Adicione pelo menos 5 Prontas Respostas antes de salvar!');
            return false;
        }
    });

    console.log('=== CLIENTES JS INICIALIZADO ===');
}); 