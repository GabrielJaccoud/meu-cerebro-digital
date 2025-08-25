# Conexões do n8n com Outras Plataformas

Este documento detalha como o n8n pode se conectar e interagir com diversas plataformas, conforme descrito no conceito do "Cérebro Digital da Queen".

## 1. GitHub

**Objetivo**: Monitorar mudanças no código, abrir issues automaticamente, etc.

**Como conectar no n8n**: Use o nó **GitHub**.

**Exemplo de Workflow**:

*   **Gatilho**: Novo commit no repositório `meu-app`.
*   **Ação**: IA (Ollama) resume as mudanças do commit.
*   **Ação**: Envia o resumo para o Telegram da Queen.
*   **Ação**: Cria uma issue no GitHub se a IA detectar um erro ou algo que precise de atenção.

## 2. Vercel

**Objetivo**: Automatizar deploys, monitorar status de deploy.

**Como conectar no n8n**: Use o nó **HTTP Request** com a API do Vercel.

**Exemplo de Workflow**:

*   **Gatilho**: Novo commit no GitHub.
*   **Ação**: Dispara um redeploy usando uma requisição `POST` para `https://api.vercel.com/v1/integrations/deploy/prj_xxx` (substitua `prj_xxx` pelo ID do seu projeto Vercel).
*   **Ação**: Aguarda o status do deploy.
*   **Ação**: Notifica a Queen via Telegram ou e-mail: "Deploy do site X concluído!" ou "Deploy do site X falhou!".

## 3. Heroku

**Objetivo**: Reiniciar aplicativos, verificar logs.

**Como conectar no n8n**: Use o nó **HTTP Request** com a API do Heroku.

**Exemplo de Workflow**:

*   **Gatilho**: Alerta de que "Heroku app X caiu" (pode ser via e-mail, Telegram, ou monitoramento externo).
*   **Ação**: Envia uma requisição `POST` para `/apps/meu-app/actions/restart-all` (substitua `meu-app` pelo nome do seu aplicativo Heroku).
*   **Ação**: Envia uma confirmação por e-mail ou Telegram sobre o reinício do aplicativo.

## 4. Unity

**Objetivo**: Automatizar builds e testes de projetos Unity.

**Como conectar no n8n**: Integre com a **Unity Cloud Build API** via nó **HTTP Request**.

**Exemplo de Workflow**:

*   **Gatilho**: Novo asset adicionado ao Google Drive.
*   **Ação**: Dispara um build na Unity Cloud Build via API.
*   **Ação**: Quando o build estiver pronto, gera um link de download.
*   **Ação**: Envia o link de download para a equipe via e-mail ou Telegram.

## 5. Google Cloud / Vertex AI

**Objetivo**: Treinar modelos de IA com seus próprios dados, usar serviços de IA avançados.

**Como conectar no n8n**: Use o nó **HTTP Request** para interagir com a API da Vertex AI.

**Exemplo de Workflow**:

*   **Gatilho**: Novo PDF de livro adicionado ao Google Drive.
*   **Ação**: Envia o PDF para a Vertex AI (ex: `automl.googleapis.com`) para processamento.
*   **Ação**: Treina um modelo de classificação com base nos conceitos do livro.
*   **Ação**: Salva os aprendizados ou o modelo treinado no Airtable.

## 6. Flux Nano Banana (Geração de Imagens com IA)

**Objetivo**: Gerar imagens para e-mails, redes sociais, banners, etc.

**Como conectar no n8n**: Use o nó **HTTP Request** com a API do Flux AI.

**Exemplo de Configuração (nó HTTP Request)**:

*   **URL**: `https://api.flux-ai.io/v1/generate`
*   **Método**: `POST`
*   **Body (JSON)**:
    ```json
    {
      "model": "nano-banana-ai",
      "prompt": "Ícone de automação com IA, estilo moderno, fundo roxo",
      "size": "1024x1024"
    }
    ```
*   **Ação Pós-Geração**: Salve a imagem gerada no Google Drive e anexe-a a e-mails ou posts.

## 7. Airtable (Memória de Longo Prazo e CRM)

**Objetivo**: Armazenar dados de leads, respostas que deram certo, sabedoria estratégica.

**Como conectar no n8n**: Use o nó **Airtable**.

**Exemplo de Uso**:

*   **Tabelas Sugeridas**: "Leads" (nome, e-mail, mensagem, idioma, projeto), "Respostas" (resposta gerada, tom, resultado, embedding), "Sabedoria Estratégica" (conceitos de livros).
*   **Busca Semântica**: Use o nó **HTTP Request** ou um nó de função para integrar com Hugging Face (`all-MiniLM-L6-v2`) para buscar semanticamente no Airtable por casos parecidos ou informações relevantes.

## 8. Gmail

**Objetivo**: Enviar e-mails personalizados, receber entradas via e-mail.

**Como conectar no n8n**: Use o nó **Gmail**.

**Exemplo de Uso**:

*   **Entrada**: Configurar um gatilho de e-mail para novas mensagens.
*   **Saída**: Enviar e-mails com texto gerado por IA e imagens anexadas.

## 9. Telegram

**Objetivo**: Enviar notificações rápidas para a Queen ou equipe.

**Como conectar no n8n**: Use o nó **Telegram**.

**Exemplo de Uso**:

*   Notificar sobre novos leads, status de deploy, erros, ou resumos de commits.

## 10. WhatsApp (via Baileys)

**Objetivo**: Receber e enviar mensagens de WhatsApp para interação com leads.

**Como conectar no n8n**: Geralmente via nó **Webhook** ou nó **HTTP Request** para uma instância do Baileys auto-hospedada.

**Exemplo de Uso**:

*   Receber mensagens de leads e disparar workflows de automação.
*   Enviar respostas personalizadas geradas por IA para os leads.

