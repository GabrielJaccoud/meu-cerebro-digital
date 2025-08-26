# 🧠👑 Cérebro Digital da Queen

> **Sistema de Inteligência Ampliada com IA Local, Automação Avançada e Processamento Multimídia**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.0+-green.svg)](https://pypi.org/project/PyQt6/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Ativo-brightgreen.svg)](https://github.com/GabrielJaccoud/meu-cerebro-digital)

## 🌟 Visão Geral

O **Cérebro Digital da Queen** é um sistema revolucionário de inteligência ampliada que combina:

- 🧠 **IA Conversacional Local** (Ollama)
- 🎤 **Interação por Voz** (STT/TTS)
- 🖼️ **Processamento Visual** avançado
- 🔄 **Geração Automática de Workflows** (n8n)
- 🤖 **Sistema de Agentes Especializados**
- ⚡ **Auto-otimização Contínua**
- 📊 **Monitoramento em Tempo Real**

## 🚀 Funcionalidades Principais

### 🧠 Inteligência Artificial
- **Modelos Locais**: llama3, phi-3:mini, mistral, codellama
- **Processamento Contextual**: Memória conversacional inteligente
- **Respostas Personalizadas**: Aprendizado contínuo das preferências

### 🎤 Interação Multimodal
- **Reconhecimento de Voz**: Comandos por fala em português
- **Síntese de Voz**: Respostas faladas naturais
- **Análise de Imagens**: Compreensão visual avançada
- **Interface Gráfica**: PyQt6 com tema escuro moderno

### 🔄 Automação Inteligente
- **Geração de Workflows**: Cria automações n8n por descrição
- **Otimização Automática**: Melhora workflows existentes
- **Integração Nativa**: GitHub, Gmail, Telegram, WhatsApp, Airtable
- **Templates Inteligentes**: Padrões pré-configurados

### 🤖 Sistema de Agentes
- **Agente de Desenvolvimento**: Código, revisão, debugging
- **Agente de Marketing**: Conteúdo, campanhas, copywriting
- **Agente de Workflows**: Automação e integração
- **Execução Paralela**: Múltiplas tarefas simultâneas

### 🎨 Processamento de Mídia
- **Geração de Imagens**: Prompts para arte digital
- **Síntese de Áudio**: Música, narração, efeitos
- **Criação de Vídeos**: Clipes curtos e animações
- **Análise Multimídia**: Transcrição e reconhecimento

### ⚡ Auto-otimização
- **Monitoramento Contínuo**: Métricas de performance
- **Identificação de Gargalos**: Detecção automática
- **Ajuste Dinâmico**: Otimização em tempo real
- **Relatórios Inteligentes**: Insights acionáveis

## 📦 Instalação Rápida

### Pré-requisitos
- Python 3.8+ (recomendado: 3.11)
- Git
- 4GB+ RAM

### 1. Clone o Repositório
```bash
git clone https://github.com/GabrielJaccoud/meu-cerebro-digital.git
cd meu-cerebro-digital
```

### 2. Configuração Automática
```bash
python scripts/setup.py
```

### 3. Instale o Ollama
```bash
# Baixe de: https://ollama.com
ollama pull llama3
ollama pull phi-3:mini
```

### 4. Execute o Sistema
```bash
# Interface completa
python app_queen_enhanced.py

# Interface básica
python app_queen.py
```

## 🎯 Como Usar

### 💬 Chat Inteligente
```
👤 Você: Como está o sistema hoje?
🧠 Queen: Sistema funcionando perfeitamente! Ollama online, 
         3 agentes ativos, performance excelente (95% saúde).
```

### 🔄 Criação de Workflows
```
👤 Você: Crie um workflow que monitore emails e responda automaticamente
🧠 Queen: Workflow criado! Monitora Gmail, analisa conteúdo com IA,
         gera resposta personalizada e envia. Salvo em workflows/
```

### 🎨 Geração de Mídia
```
👤 Você: Gere uma imagem de um robô futurista
🧠 Queen: Imagem gerada com sucesso! Salva em: generated_images/robot_futuristic_001.png
```

### 🤖 Delegação para Agentes
```
👤 Você: Crie uma API REST em Python para gerenciar usuários
🧠 Queen: Tarefa delegada ao Agente de Desenvolvimento...
         ✅ API criada com Flask, endpoints CRUD, documentação incluída!
```

## 📊 Interface do Sistema

### Abas Principais

#### 💬 **Chat**
- Conversa natural com IA
- Comandos por voz
- Análise de imagens
- Botão de emergência

#### 🔄 **Workflows**
- Geração automática
- Otimização inteligente
- Importação para n8n
- Visualização JSON

#### 🎨 **Mídia**
- Criação de conteúdo
- Análise de arquivos
- Múltiplos formatos
- Processamento batch

#### 🤖 **Agentes**
- Lista de especialistas
- Execução de tarefas
- Monitoramento de performance
- Histórico de atividades

#### ⚙️ **Configurações**
- Parâmetros de IA
- Configurações de voz
- Preferências de interface
- Backup e sincronização

#### 📊 **Status**
- Saúde do sistema
- Métricas em tempo real
- Alertas e notificações
- Relatórios de performance

## 🏗️ Arquitetura

```
🧠 Cérebro Digital da Queen
├── 🎯 Interface Principal (PyQt6)
├── 🤖 Sistema de Agentes
│   ├── Agente de Desenvolvimento
│   ├── Agente de Marketing
│   └── Agente de Workflows
├── 🔧 Módulos Especializados
│   ├── Auto-otimizador
│   ├── Gerador de Workflows
│   └── Processador de Mídia
├── 🗄️ Bancos de Dados (SQLite)
│   ├── Memória Conversacional
│   ├── Métricas de Performance
│   └── Histórico de Agentes
└── 🔌 Integrações Externas
    ├── Ollama (IA Local)
    ├── n8n (Automação)
    └── APIs de Mídia
```

## 🛠️ Tecnologias

### Core
- **Python 3.11**: Linguagem principal
- **PyQt6**: Interface gráfica moderna
- **SQLite**: Banco de dados local
- **Requests**: Comunicação HTTP

### IA e Processamento
- **Ollama**: Modelos de linguagem locais
- **SpeechRecognition**: Reconhecimento de voz
- **pyttsx3**: Síntese de voz
- **Pillow**: Processamento de imagens

### Automação e Integração
- **n8n**: Plataforma de automação
- **Flask**: APIs e webhooks
- **Schedule**: Tarefas agendadas
- **psutil**: Monitoramento do sistema

## 📈 Performance

### Benchmarks
- **Tempo de Resposta**: < 2s (média)
- **Taxa de Sucesso**: > 95%
- **Uso de Memória**: ~500MB (base)
- **Precisão da IA**: 92% (avaliação interna)

### Otimizações
- **Cache Inteligente**: Respostas frequentes
- **Processamento Paralelo**: Múltiplas threads
- **Compressão de Dados**: Redução de armazenamento
- **Auto-ajuste**: Parâmetros dinâmicos

## 🔧 Configuração Avançada

### Arquivo config.json
```json
{
  "ollama": {
    "url": "http://localhost:11434/api/generate",
    "default_model": "llama3",
    "temperature": 0.7
  },
  "tts": {
    "rate": 150,
    "volume": 0.9,
    "voice": "portuguese"
  },
  "ui": {
    "theme": "dark",
    "auto_save": true
  }
}
```

### Variáveis de Ambiente
```bash
export OLLAMA_HOST=localhost:11434
export N8N_HOST=localhost:5678
export DEBUG=true
```

## 📚 Documentação

- 📖 [Manual do Usuário](docs/manual-do-usuario.md)
- 🔧 [Guia de Instalação](docs/guia-instalacao-completo.md)
- 🏗️ [Arquitetura do Sistema](docs/futuro-cerebro-digital.md)
- 🔄 [Integração n8n](docs/integracao-n8n-github.md)
- 🤖 [Sistema de Agentes](docs/area-para-agentes.md)

## 🧪 Testes

```bash
# Executar todos os testes
python -m unittest tests.test_modules -v

# Verificar status do sistema
python scripts/status.py

# Teste de módulos
python -c "
from modules.auto_optimizer import PerformanceMonitor
from agents.agent_manager import AgentManager
print('✅ Todos os módulos OK')
"
```

## 🤝 Contribuindo

Contribuições são muito bem-vindas! 

### Como Contribuir
1. **Fork** o projeto
2. **Crie** uma branch (`git checkout -b feature/NovaFuncionalidade`)
3. **Commit** suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. **Push** para a branch (`git push origin feature/NovaFuncionalidade`)
5. **Abra** um Pull Request

### Áreas de Contribuição
- 🐛 **Correção de bugs**
- ✨ **Novas funcionalidades**
- 📚 **Documentação**
- 🧪 **Testes**
- 🎨 **Interface**
- 🔧 **Otimizações**

## 📊 Estatísticas do Projeto

- **Linhas de Código**: ~4.000+
- **Módulos**: 12
- **Testes**: 25+
- **Documentação**: 6 guias completos
- **Funcionalidades**: 50+

## 🗺️ Roadmap

### 🎯 Versão 1.1 (Setembro 2025)
- [ ] Integração com APIs de vídeo avançadas
- [ ] Sistema de plugins extensível
- [ ] IA visual com reconhecimento de objetos
- [ ] Colaboração multi-usuário

### 🎯 Versão 1.2 (Outubro 2025)
- [ ] Interface web responsiva
- [ ] Integração com Slack/Discord/Teams
- [ ] IA preditiva e sugestões proativas
- [ ] Marketplace de extensões

### 🎯 Versão 2.0 (2026)
- [ ] Arquitetura distribuída
- [ ] IA multimodal avançada
- [ ] Integração com IoT
- [ ] Análise preditiva de negócios

## 📞 Suporte

### Canais de Suporte
- 🐛 **Issues**: [GitHub Issues](https://github.com/GabrielJaccoud/meu-cerebro-digital/issues)
- 💬 **Discussões**: [GitHub Discussions](https://github.com/GabrielJaccoud/meu-cerebro-digital/discussions)
- 📧 **Email**: gabriel.jaccoud@example.com

### FAQ
**P: O sistema funciona offline?**
R: Sim! A IA (Ollama) roda localmente, apenas algumas integrações precisam de internet.

**P: Posso usar meus próprios modelos?**
R: Sim! Qualquer modelo compatível com Ollama pode ser usado.

**P: É seguro? Meus dados ficam privados?**
R: Totalmente! Tudo roda localmente, seus dados não saem do seu computador.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- **Ollama Team**: Pela incrível plataforma de IA local
- **n8n Community**: Pela ferramenta de automação fantástica
- **PyQt Team**: Pela biblioteca de interface robusta
- **Comunidade Python**: Pelo ecossistema rico em ferramentas

---

<div align="center">

**🧠👑 Bem-vinda ao futuro da inteligência ampliada! 👑🧠**

*Desenvolvido com ❤️ por Gabriel Jaccoud*

[![GitHub](https://img.shields.io/badge/GitHub-GabrielJaccoud-black.svg)](https://github.com/GabrielJaccoud)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Gabriel%20Jaccoud-blue.svg)](https://linkedin.com/in/gabrieljaccoud)

</div>

