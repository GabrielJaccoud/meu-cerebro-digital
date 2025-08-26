# 🧠👑 Guia Completo de Instalação - Cérebro Digital da Queen

## 📋 Pré-requisitos

### Sistema Operacional
- **Windows 10/11** (recomendado)
- **Linux Ubuntu 20.04+** 
- **macOS 10.15+**

### Software Necessário
- **Python 3.8+** (recomendado: Python 3.11)
- **Git** para controle de versão
- **Docker** (opcional, para n8n)

## 🚀 Instalação Rápida

### 1. Clone o Repositório
```bash
git clone https://github.com/GabrielJaccoud/meu-cerebro-digital.git
cd meu-cerebro-digital
```

### 2. Execute o Setup Automático
```bash
python scripts/setup.py
```

### 3. Inicie o Aplicativo
```bash
python app_queen.py
```

## 🔧 Instalação Detalhada

### Passo 1: Preparação do Ambiente

#### Windows
1. Instale Python 3.11 do [site oficial](https://python.org)
2. Instale Git do [site oficial](https://git-scm.com)
3. Abra o PowerShell como Administrador

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.11 python3.11-pip git
```

#### macOS
```bash
# Instale Homebrew se não tiver
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instale Python e Git
brew install python@3.11 git
```

### Passo 2: Clone e Configuração

```bash
# Clone o repositório
git clone https://github.com/GabrielJaccoud/meu-cerebro-digital.git
cd meu-cerebro-digital

# Crie ambiente virtual (recomendado)
python -m venv venv

# Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Instale dependências
pip install -r requirements.txt
```

### Passo 3: Configuração dos Serviços

#### Ollama (IA Local)
1. Baixe e instale do [site oficial](https://ollama.com)
2. Inicie o Ollama:
   ```bash
   ollama serve
   ```
3. Baixe os modelos necessários:
   ```bash
   ollama pull llama3
   ollama pull phi-3:mini
   ```

#### n8n (Automação - Opcional)
```bash
# Usando Docker
docker run -d --name n8n -p 5678:5678 n8nio/n8n

# Ou usando npm
npm install -g n8n
n8n start
```

### Passo 4: Configuração Inicial

Execute o script de configuração:
```bash
python scripts/setup.py
```

Este script irá:
- ✅ Verificar dependências
- ✅ Criar diretórios necessários
- ✅ Inicializar bancos de dados
- ✅ Criar arquivo de configuração
- ✅ Testar conexões

## 🎯 Verificação da Instalação

Execute o script de status:
```bash
python scripts/status.py
```

Você deve ver:
- 🟢 Python: Compatível
- 🟢 Dependências: Instaladas
- 🟢 Bancos de dados: Inicializados
- 🟢 Arquivos: Presentes

## 🚀 Primeira Execução

### Modo Desktop (Interface Gráfica)
```bash
python app_queen.py
```

### Modo Aprimorado (Todas as Funcionalidades)
```bash
python app_queen_enhanced.py
```

### Modo Linha de Comando (Teste)
```bash
python -c "
from modules.auto_optimizer import PerformanceMonitor
monitor = PerformanceMonitor()
print('✅ Sistema funcionando!')
"
```

## 🔧 Configuração Avançada

### Arquivo de Configuração (config.json)

O arquivo `config.json` é criado automaticamente com as configurações padrão:

```json
{
  "ollama": {
    "url": "http://localhost:11434/api/generate",
    "default_model": "llama3",
    "models": ["phi-3:mini", "llama3", "mistral"]
  },
  "n8n": {
    "url": "http://localhost:5678/api/v1",
    "webhook_url": "http://localhost:5678/webhook"
  },
  "tts": {
    "engine": "pyttsx3",
    "rate": 150,
    "volume": 0.9,
    "voice": "portuguese"
  },
  "ui": {
    "theme": "dark",
    "window_size": [800, 600],
    "auto_save": true
  }
}
```

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:
```env
# APIs (opcional)
OPENAI_API_KEY=sua_chave_aqui
GITHUB_TOKEN=seu_token_aqui

# Configurações
DEBUG=true
LOG_LEVEL=INFO
```

## 🐛 Solução de Problemas

### Erro: "No module named 'PyQt6'"
```bash
pip install PyQt6
```

### Erro: "Could not load Qt platform plugin"
**Linux:**
```bash
sudo apt install libxcb-cursor0
```

**Ou execute sem interface gráfica:**
```bash
export QT_QPA_PLATFORM=offscreen
python app_queen.py
```

### Erro: "Ollama connection refused"
1. Verifique se o Ollama está rodando:
   ```bash
   ollama serve
   ```
2. Teste a conexão:
   ```bash
   curl http://localhost:11434/api/tags
   ```

### Erro: "n8n not found"
```bash
# Usando Docker
docker run -d -p 5678:5678 n8nio/n8n

# Ou instale localmente
npm install -g n8n
```

### Problemas de Áudio (TTS/STT)
**Windows:**
- Instale Microsoft Visual C++ Redistributable

**Linux:**
```bash
sudo apt install espeak espeak-data libespeak1 libespeak-dev
sudo apt install portaudio19-dev python3-pyaudio
```

**macOS:**
```bash
brew install portaudio
```

## 📊 Monitoramento e Logs

### Verificar Status
```bash
python scripts/status.py
```

### Logs do Sistema
Os logs são salvos em:
- `logs/queen.log` - Log principal
- `logs/performance.log` - Métricas de performance
- `logs/agents.log` - Atividade dos agentes

### Métricas de Performance
```bash
# Ver métricas em tempo real
python -c "
from modules.auto_optimizer import PerformanceMonitor
monitor = PerformanceMonitor()
print(monitor.get_metric_trend('response_time', 24))
"
```

## 🔄 Atualizações

### Atualizar o Código
```bash
git pull origin master
pip install -r requirements.txt --upgrade
```

### Atualizar Modelos do Ollama
```bash
ollama pull llama3
ollama pull phi-3:mini
```

### Backup dos Dados
```bash
# Backup automático
python -c "
import shutil
import datetime
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
shutil.copy('queen_memory.db', f'backups/queen_memory_{timestamp}.db')
print('Backup criado!')
"
```

## 🆘 Suporte

### Documentação Adicional
- [Como usar o n8n](docs/como-importar-no-n8n.md)
- [Integração com GitHub](docs/integracao-n8n-github.md)
- [Área para Agentes](docs/area-para-agentes.md)
- [Funcionalidades Futuras](docs/futuro-cerebro-digital.md)

### Comunidade
- **GitHub Issues**: [Reportar problemas](https://github.com/GabrielJaccoud/meu-cerebro-digital/issues)
- **Discussões**: [GitHub Discussions](https://github.com/GabrielJaccoud/meu-cerebro-digital/discussions)

### Contato
- **Desenvolvedor**: Gabriel Jaccoud
- **Repositório**: https://github.com/GabrielJaccoud/meu-cerebro-digital

---

## 🎉 Pronto!

Agora você tem o **Cérebro Digital da Queen** funcionando com todas as funcionalidades:

- 🧠 **Inteligência Artificial Local** (Ollama)
- 🎤 **Reconhecimento de Voz**
- 🔊 **Síntese de Voz**
- 🖼️ **Processamento de Imagens**
- 🔄 **Geração de Workflows**
- 🤖 **Sistema de Agentes**
- ⚡ **Auto-otimização**
- 📊 **Monitoramento de Performance**

**Bem-vinda ao futuro da automação inteligente!** 👑

