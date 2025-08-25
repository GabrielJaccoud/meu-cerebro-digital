# Como Iniciar o n8n e o Ollama Localmente

Este guia detalha os passos para configurar e iniciar o n8n (orquestrador) e o Ollama (IA local) em seu ambiente, preferencialmente em um sistema Ubuntu 24.04 com Docker.

## 1. Infraestrutura Local (Ubuntu 24.04 + Docker)

Certifique-se de que seu sistema Ubuntu esteja atualizado e que o Docker esteja instalado e configurado. Se ainda não tiver o Docker, siga os comandos abaixo:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install docker.io docker-compose -y
sudo systemctl enable docker
sudo usermod -aG docker $USER
newgrp docker
```

Estes comandos atualizam seu sistema, instalam o Docker e o Docker Compose, habilitam o serviço Docker e adicionam seu usuário ao grupo `docker` para que você possa executar comandos Docker sem `sudo`. O `newgrp docker` é para aplicar as mudanças de grupo imediatamente.

## 2. Iniciar o n8n (Orquestrador)

Com o Docker instalado, você pode iniciar o n8n com um único comando. O n8n será executado em um contêiner Docker, isolado do seu sistema principal.

```bash
docker run -d -p 5678:5678 \
  -e N8N_BASIC_AUTH_USER=queen \
  -e N8N_BASIC_AUTH_PASSWORD=brilhe \
  --name n8n \
  n8nio/n8n
```

**Explicação do comando:**
*   `-d`: Executa o contêiner em modo `detached` (em segundo plano).
*   `-p 5678:5678`: Mapeia a porta 5678 do seu host para a porta 5678 do contêiner, permitindo que você acesse o n8n pelo navegador.
*   `-e N8N_BASIC_AUTH_USER=queen`: Define o nome de usuário para acesso básico ao n8n como `queen`.
*   `-e N8N_BASIC_AUTH_PASSWORD=brilhe`: Define a senha para acesso básico ao n8n como `brilhe`.
*   `--name n8n`: Atribui o nome `n8n` ao contêiner para facilitar o gerenciamento.
*   `n8nio/n8n`: Especifica a imagem Docker oficial do n8n.

Após executar o comando, o n8n estará acessível em seu navegador em `http://localhost:5678`. Use as credenciais `queen` / `brilhe` para fazer login.

## 3. Instalar e Iniciar o Ollama (IA Local)

O Ollama permite que você execute modelos de linguagem grandes (LLMs) localmente. Siga os passos para instalá-lo e baixar alguns modelos:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Este comando baixa e executa o script de instalação do Ollama. Após a instalação, você pode baixar e executar modelos de IA. Os modelos sugeridos são `phi-3`, `llama3` e `mistral`:

```bash
ollama run phi-3:mini
ollama run llama3
ollama run mistral
```

O primeiro comando para cada modelo irá baixá-lo (se ainda não estiver presente) e iniciá-lo. Você pode testar o Ollama com um prompt simples:

```bash
ollama run phi-3:mini "Escreva uma mensagem em espanhol para um lead interessado em automação."
```

Com o n8n e o Ollama em funcionamento, você terá a base para construir seu "Cérebro Digital da Queen" e começar a integrar as IAs locais em seus workflows.

