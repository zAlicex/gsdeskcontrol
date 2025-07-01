document.addEventListener('DOMContentLoaded', function() {
    console.log('=== JAVASCRIPT CARREGADO ===');
    
    // Elementos do DOM
    const form = document.getElementById('clienteForm');
    const formTitle = document.getElementById('formTitle');
    const submitBtn = document.getElementById('submitBtn');
    const clienteIdField = document.getElementById('cliente_id');
    const cancelBtn = document.getElementById('cancelEdit');
    const limparBtn = document.getElementById('limparForm');
    const listContainer = document.getElementById('client-list-container');
    const loadingIndicator = document.getElementById('loading-indicator');

    console.log('Elementos encontrados:', {
        form: !!form,
        formTitle: !!formTitle,
        submitBtn: !!submitBtn,
        clienteIdField: !!clienteIdField,
        listContainer: !!listContainer
    });

    if (!form || !listContainer) {
        console.error('Elementos essenciais não encontrados!');
        return;
    }

    const CREATE_URL = form.action;
    const UPDATE_URL_TEMPLATE = listContainer.dataset.updateUrlTemplate;
    const GET_CLIENT_URL_TEMPLATE = listContainer.dataset.getUrlTemplate;
    
    console.log('URLs configuradas:', {
        CREATE_URL,
        UPDATE_URL_TEMPLATE,
        GET_CLIENT_URL_TEMPLATE
    });

    // Variáveis para scroll infinito
    let isLoading = false;
    let hasMore = true;
    let currentOffset = 0;
    const limit = 20;

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

        // Lista de todos os campos do formulário que são preenchidos dinamicamente
        const camposParaLimpar = [
            'numero_os', 'data_chamado', 'status_servico', 'nome',
            'cpf_cnpj', 'telefone', 'celular', 'email', 'apto_bloco',
            'endereco', 'bairro', 'cidade', 'cep', 'revendedor',
            'tecnicos', 'periodo', 'data_instalacao', 'valor_total',
            'forma_pagamento', 'servicos', 'relatorios_servicos_prestados'
        ];
        
        // Limpa cada campo individualmente para garantir
        camposParaLimpar.forEach(campoId => {
            const elemento = document.getElementById(campoId);
            if (elemento) {
                if (elemento.tagName.toLowerCase() === 'select') {
                    elemento.selectedIndex = 0; // Para selects, volta para a primeira opção
                } else {
                    elemento.value = ''; // Para inputs e textareas
                }
            }
        });
        
        // Reseta o formulário (pode ser redundante, mas é uma boa prática)
        if(form) form.reset();

        // Reseta os campos e botões específicos da interface
        if(clienteIdField) clienteIdField.value = '';
        if(formTitle) formTitle.textContent = 'Novo Cliente';
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
     * Carrega mais clientes via scroll infinito
     */
    async function loadMoreClientes() {
        if (isLoading || !hasMore) return;

        isLoading = true;
        if (loadingIndicator) {
            loadingIndicator.style.display = 'block';
        }

        try {
            const searchName = document.getElementById('search-name-input')?.value || '';
            const searchOs = document.getElementById('search-os-input')?.value || '';

            const params = new URLSearchParams({
                offset: currentOffset,
                limit: limit,
                search_name: searchName,
                search_os: searchOs
            });

            const response = await fetch(`/clientes/carregar-mais/?${params}`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCSRFToken()
                }
            });

            if (response.ok) {
                const data = await response.json();
                
                if (data.html) {
                    // Remove o indicador de loading
                    if (loadingIndicator) {
                        loadingIndicator.remove();
                    }
                    
                    // Adiciona os novos itens antes do indicador de loading
                    const tempDiv = document.createElement('div');
                    tempDiv.innerHTML = data.html;
                    
                    // Remove o indicador de loading do HTML recebido
                    const loadingFromResponse = tempDiv.querySelector('#loading-indicator');
                    if (loadingFromResponse) {
                        loadingFromResponse.remove();
                    }
                    
                    // Adiciona os novos itens
                    listContainer.appendChild(tempDiv);
                    
                    // Re-adiciona o indicador de loading
                    if (loadingIndicator) {
                        listContainer.appendChild(loadingIndicator);
                    }
                }
                
                hasMore = data.has_more;
                currentOffset += limit;
                
                console.log(`Carregados mais ${limit} clientes. Total: ${currentOffset}`);
            } else {
                console.error('Erro ao carregar mais clientes:', response.status);
            }
        } catch (error) {
            console.error('Erro ao carregar mais clientes:', error);
        } finally {
            isLoading = false;
            if (loadingIndicator) {
                loadingIndicator.style.display = 'none';
            }
        }
    }

    /**
     * Função para detectar quando o usuário chegou próximo ao final da lista
     */
    function handleScroll() {
        const scrollTop = listContainer.scrollTop;
        const scrollHeight = listContainer.scrollHeight;
        const clientHeight = listContainer.clientHeight;
        
        // Carrega mais quando está a 100px do final
        if (scrollHeight - scrollTop - clientHeight < 100) {
            loadMoreClientes();
        }
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

    // Adiciona listener de scroll para scroll infinito
    if (listContainer) {
        listContainer.addEventListener('scroll', handleScroll);
    }

    /**
     * Lida com o clique fora do formulário e da lista para resetar o estado de edição.
     */
    document.addEventListener('click', function(event) {
        // Pega as duas colunas principais
        const formColumn = document.getElementById('form-column');
        const listColumn = document.getElementById('list-column');
        
        // Verifica se o formulário está em modo de edição (o botão 'Voltar' está visível)
        const isInEditMode = cancelBtn && cancelBtn.style.display !== 'none';

        if (isInEditMode && formColumn && listColumn) {
            // Verifica se o clique ocorreu fora da coluna do formulário E fora da coluna da lista
            const clickedOutside = !formColumn.contains(event.target) && !listColumn.contains(event.target);

            if (clickedOutside) {
                console.log('Clique fora da área de conteúdo detectado. Resetando formulário.');
                resetFormToCreateMode();
            }
        }
    });

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

    console.log('=== JAVASCRIPT INICIALIZADO COMPLETAMENTE ===');
}); 