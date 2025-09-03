# 🧠 Workflow n8n: Atendimento e Vendas do Livro Mostardinha

## 💡 Visão Geral do Design

Este documento detalha o design de um workflow no n8n para automatizar o atendimento e as vendas do livro "Mostardinha", integrando interações via site e WhatsApp. O objetivo é criar um sistema inteligente e autônomo que possa responder a perguntas frequentes, direcionar para a compra, e escalar para atendimento humano quando necessário, utilizando o Ollama para inteligência artificial local.

## 🎯 Objetivos do Workflow

-   **Automatizar Respostas:** Fornecer respostas rápidas e precisas a perguntas frequentes sobre o livro.
-   **Facilitar Vendas:** Redirecionar clientes interessados para a página de compra na Hotmart.
-   **Capturar Leads:** Registrar informações de contato de potenciais clientes.
-   **Escalar Atendimento:** Direcionar conversas complexas ou sensíveis para um atendente humano.
-   **Personalizar Interações:** Oferecer respostas contextualizadas e amigáveis.

## 🚀 Estrutura do Workflow (Nós Principais)

O workflow será construído em torno de um fluxo principal que se ramifica com base na intenção do usuário. Abaixo, descrevemos os nós e suas funcionalidades:

### 1. **Trigger (Gatilho): Entrada de Mensagens/Dados**

Este é o ponto de entrada do workflow, onde as interações dos clientes são recebidas.

-   **Webhook (WhatsApp):**
    -   **Propósito:** Receber mensagens dos clientes via WhatsApp. Requer uma API de WhatsApp Business (ex: Twilio, 360Dialog) configurada para enviar mensagens para este webhook do n8n.
    -   **Configuração:** Um nó `Webhook` configurado para escutar em um caminho específico (ex: `/whatsapp-mostardinha`). Ele receberá o corpo da mensagem, o número do remetente e outras informações relevantes.
-   **Webhook (Site - Formulário de Contato):**
    -   **Propósito:** Capturar submissões do formulário "Fale Conosco" do site.
    -   **Configuração:** Outro nó `Webhook` configurado para receber dados (Nome, E-mail, Mensagem) do formulário do site.

### 2. **Processamento Inicial e Normalização**

Após o gatilho, os dados são preparados para análise.

-   **Set (Normalização de Dados):**
    -   **Propósito:** Padronizar o formato dos dados recebidos de diferentes fontes (WhatsApp, formulário do site) para que o Ollama e outros nós possam processá-los consistentemente.
    -   **Configuração:** Criar campos como `customer_name`, `customer_contact` (número do WhatsApp ou e-mail), `message_text`, `source_channel` (WhatsApp/Site).

### 3. **Inteligência Artificial (Ollama): Análise de Intenção e Geração de Resposta**

O coração da inteligência do workflow, utilizando o Ollama para entender e responder.

-   **Ollama (Classificação de Intenção):**
    -   **Propósito:** Analisar a `message_text` do cliente para classificar a intenção (ex: `FAQ_Preco`, `FAQ_Conteudo`, `Compra_Interesse`, `Suporte_Problema`, `Falar_Humano`, `Outro`).
    -   **Configuração:** Um nó `Ollama` com um prompt que instrui o modelo a classificar a mensagem e retornar a intenção em um formato estruturado (ex: JSON).
    -   **Exemplo de Prompt:**
        ```
        Você é um assistente de IA para o livro 'Mostardinha'. Classifique a intenção da seguinte mensagem do cliente em uma das categorias: FAQ_Preco, FAQ_Conteudo, FAQ_Formato, Compra_Interesse, Suporte_Problema, Falar_Humano, Outro. Retorne apenas a categoria. Mensagem: "{{ $json.message_text }}"
        ```
-   **Ollama (Geração de Resposta/Conteúdo):**
    -   **Propósito:** Gerar respostas detalhadas e contextualizadas com base na intenção classificada e no banco de conhecimento.
    -   **Configuração:** Múltiplos nós `Ollama` ou um único nó com lógica condicional para prompts diferentes, dependendo da intenção. Estes nós consultarão o banco de conhecimento (ver item 4).

### 4. **Banco de Conhecimento (Knowledge Base)**

Armazena todas as informações sobre o livro e FAQs.

-   **Google Sheets / Airtable (ou JSON estático no n8n):**
    -   **Propósito:** Armazenar perguntas frequentes, respostas, sinopse do livro, links de compra, informações de contato, etc.
    -   **Configuração:** Nós `Google Sheets` ou `Airtable` para buscar informações. Para um banco de conhecimento menor e estático, um nó `Function` com um JSON embutido pode ser suficiente.
    -   **Exemplo de Dados:**
        ```json
        {
          


  "faqs": [
            {"pergunta": "Quanto custa o livro?", "resposta": "O livro Mostardinha custa R$ 34,99. Você pode comprar aqui: https://pay.hotmart.com/H100940670E"},
            {"pergunta": "Sobre o que é o livro?", "resposta": "Mostardinha é um livro infantil que aborda temas socioemocionais..."}
          ],
          "livro_info": {
            "titulo": "Mostardinha",
            "autor": "Gabriel Jaccoud",
            "preco": "R$ 34,99",
            "link_hotmart": "https://pay.hotmart.com/H100940670E",
            "link_audiobook": "https://www.youtube.com/watch?v=BSzPFZICl5c"
          }
        }
        ```

### 5. **Lógica Condicional (If/Switch)**

Direciona o fluxo do workflow com base na intenção identificada pelo Ollama.

-   **If (Intenção):**
    -   **Propósito:** Criar ramificações para diferentes tipos de intenção (FAQ, Compra, Suporte, Falar Humano).
    -   **Configuração:** Um nó `If` que verifica o valor da intenção retornada pelo Ollama.

### 6. **Fluxo de Respostas FAQ**

Para perguntas frequentes, o sistema responde automaticamente.

-   **Function (Formatar Resposta FAQ):**
    -   **Propósito:** Combinar a resposta gerada pelo Ollama com informações do banco de conhecimento e formatar a mensagem final para o cliente.
    -   **Configuração:** Um nó `Function` que constrói a mensagem, adicionando links relevantes (Hotmart, audiobook) e personalização (ex: nome do cliente).
-   **WhatsApp (Enviar Mensagem):**
    -   **Propósito:** Enviar a resposta formatada de volta para o cliente via WhatsApp.
    -   **Configuração:** Um nó `WhatsApp` (ou o nó correspondente à API de WhatsApp Business que você estiver usando) que envia a `message_text` para o `customer_contact`.

### 7. **Fluxo de Vendas (Redirecionamento para Hotmart)**

Para intenções de compra, o cliente é direcionado.

-   **Function (Gerar Link de Compra):**
    -   **Propósito:** Criar uma mensagem convidativa com o link direto para a Hotmart.
    -   **Configuração:** Um nó `Function` que usa o `link_hotmart` do banco de conhecimento.
-   **WhatsApp (Enviar Mensagem):**
    -   **Propósito:** Enviar a mensagem com o link de compra.

### 8. **Fluxo de Suporte e Escalação Humana**

Para casos que exigem intervenção humana.

-   **If (Confiança/Pedido Explícito):**
    -   **Propósito:** Verificar se a confiança do Ollama é baixa ou se o cliente pediu para falar com um humano.
    -   **Configuração:** Um nó `If` que verifica o `confidence_score` retornado pelo Ollama (se implementado) ou palavras-chave como "humano", "atendente", "ajuda urgente" na `message_text`.
-   **Google Sheets / Airtable (Registrar Lead/Suporte):**
    -   **Propósito:** Registrar a conversa e os dados do cliente para acompanhamento humano.
    -   **Configuração:** Um nó `Google Sheets` ou `Airtable` para adicionar uma nova linha com `customer_name`, `customer_contact`, `message_text`, `status` (ex: "Pendente Atendimento Humano").
-   **Telegram / Gmail (Notificação Interna):**
    -   **Propósito:** Notificar o atendente humano sobre a necessidade de intervenção.
    -   **Configuração:** Um nó `Telegram` ou `Gmail` para enviar uma mensagem/e-mail para um grupo ou endereço específico, contendo os detalhes do cliente e da conversa.
-   **WhatsApp (Mensagem de Confirmação ao Cliente):**
    -   **Propósito:** Informar ao cliente que sua solicitação foi recebida e que um atendente entrará em contato em breve.

### 9. **Registro de Leads e Histórico de Conversas**

Para manter um registro de todas as interações.

-   **Google Sheets / Airtable (Registrar Conversa):**
    -   **Propósito:** Salvar cada interação (entrada do cliente e resposta do sistema) para análise futura e histórico.
    -   **Configuração:** Um nó `Google Sheets` ou `Airtable` que adiciona uma nova linha com `timestamp`, `customer_contact`, `message_text`, `ai_response`, `intention`, etc.

## 🔄 Fluxo Detalhado (Exemplo: WhatsApp - FAQ)

1.  **Webhook (WhatsApp):** Recebe a mensagem do cliente.
2.  **Set (Normalização):** Extrai `customer_name`, `customer_contact`, `message_text`.
3.  **Ollama (Classificação de Intenção):** Analisa `message_text` e retorna `intention` (ex: `FAQ_Preco`).
4.  **If (Intenção):** Verifica se `intention` é `FAQ_Preco`.
    -   **TRUE:**
        5.  **Google Sheets / Airtable (Buscar Preço):** Consulta o banco de conhecimento para obter o preço e o link da Hotmart.
        6.  **Function (Formatar Resposta):** Constrói a mensagem: "O livro Mostardinha custa R$ 34,99. Você pode comprar aqui: [link Hotmart]."
        7.  **WhatsApp (Enviar Mensagem):** Envia a resposta ao cliente.
    -   **FALSE:**
        8.  **If (Outras Intenções):** Continua a ramificação para outras intenções (FAQ_Conteudo, Compra_Interesse, etc.).

## ⚠️ Tratamento de Erros e Fallback

-   **Ollama Falha:** Se o Ollama não conseguir classificar a intenção ou gerar uma resposta com confiança suficiente, o workflow deve escalar para um atendente humano.
-   **Integrações Externas:** Implementar tratamento de erros para falhas de conexão com Hotmart (se houver webhook), WhatsApp API, Google Sheets/Airtable. Notificar internamente sobre falhas.
-   **Mensagens Não Compreendidas:** Se a intenção for `Outro` ou se o Ollama retornar baixa confiança, o sistema pode pedir mais informações ao cliente ou escalar para humano.

## 📈 Otimizações Futuras

-   **Personalização Avançada:** Usar o nome do cliente em todas as interações.
-   **Histórico de Conversas:** Integrar com o `queen_memory.db` para um histórico mais rico e contextualizado.
-   **Notificações Pós-Compra:** Enviar mensagens de boas-vindas e dicas de uso do livro após a confirmação de compra da Hotmart.
-   **Pesquisa de Satisfação:** Enviar uma pesquisa rápida após o atendimento.

Este design fornece uma base sólida para o workflow do n8n. As configurações específicas de cada nó (APIs, credenciais, URLs) precisarão ser preenchidas no n8n.

