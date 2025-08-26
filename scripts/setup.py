# scripts/setup.py
"""
Script de configuração inicial do Cérebro Digital da Queen
"""

import os
import sys
import subprocess
import sqlite3
import json
from pathlib import Path

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário")
        return False
    print(f"✅ Python {sys.version.split()[0]} detectado")
    return True

def install_dependencies():
    """Instala dependências Python"""
    print("📦 Instalando dependências...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def check_ollama():
    """Verifica se Ollama está instalado e rodando"""
    print("🤖 Verificando Ollama...")
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama está rodando")
            return True
        else:
            print("⚠️  Ollama não está respondendo")
            return False
    except Exception:
        print("❌ Ollama não encontrado. Instale em: https://ollama.com")
        return False

def check_n8n():
    """Verifica se n8n está disponível"""
    print("🔄 Verificando n8n...")
    
    try:
        import requests
        response = requests.get("http://localhost:5678", timeout=5)
        if response.status_code == 200:
            print("✅ n8n está rodando")
            return True
        else:
            print("⚠️  n8n não está respondendo")
            return False
    except Exception:
        print("❌ n8n não encontrado. Execute: docker run -d -p 5678:5678 n8nio/n8n")
        return False

def create_directories():
    """Cria diretórios necessários"""
    print("📁 Criando diretórios...")
    
    directories = [
        "generated_images",
        "generated_audio",
        "generated_videos",
        "refined_images",
        "workflows/generated",
        "logs",
        "backups"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Diretórios criados")

def initialize_databases():
    """Inicializa bancos de dados SQLite"""
    print("🗄️  Inicializando bancos de dados...")
    
    # Banco principal da Queen
    conn = sqlite3.connect('queen_memory.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT,
            response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            user_input TEXT,
            ai_response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    
    # Banco de performance
    conn = sqlite3.connect('queen_performance.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            metric_name TEXT NOT NULL,
            metric_value REAL NOT NULL,
            context TEXT
        )
    """)
    
    conn.commit()
    conn.close()
    
    # Banco de agentes
    conn = sqlite3.connect('agents.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agent_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_id TEXT NOT NULL,
            task_type TEXT NOT NULL,
            task_data TEXT NOT NULL,
            status TEXT NOT NULL,
            result TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            completed_at DATETIME
        )
    """)
    
    conn.commit()
    conn.close()
    
    print("✅ Bancos de dados inicializados")

def create_config_file():
    """Cria arquivo de configuração"""
    print("⚙️  Criando arquivo de configuração...")
    
    config = {
        "ollama": {
            "url": "http://localhost:11434/api/generate",
            "default_model": "llama3",
            "models": ["phi-3:mini", "llama3", "mistral"]
        },
        "n8n": {
            "url": "http://localhost:5678/api/v1",
            "webhook_url": "http://localhost:5678/webhook"
        },
        "apis": {
            "flux_ai": {
                "url": "https://api.flux-ai.io/v1/generate",
                "api_key": ""
            },
            "github": {
                "token": "",
                "repo": "meu-cerebro-digital"
            }
        },
        "tts": {
            "engine": "pyttsx3",
            "rate": 150,
            "volume": 0.9,
            "voice": "portuguese"
        },
        "speech_recognition": {
            "engine": "google",
            "language": "pt-BR",
            "timeout": 5
        },
        "ui": {
            "theme": "dark",
            "window_size": [800, 600],
            "auto_save": True
        }
    }
    
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("✅ Arquivo de configuração criado")

def download_models():
    """Baixa modelos necessários do Ollama"""
    print("🧠 Verificando modelos do Ollama...")
    
    models = ["phi-3:mini", "llama3"]
    
    for model in models:
        print(f"Verificando modelo {model}...")
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
            if model in result.stdout:
                print(f"✅ Modelo {model} já está disponível")
            else:
                print(f"📥 Baixando modelo {model}...")
                subprocess.run(["ollama", "pull", model], check=True)
                print(f"✅ Modelo {model} baixado")
        except subprocess.CalledProcessError:
            print(f"❌ Erro ao baixar modelo {model}")
        except FileNotFoundError:
            print("❌ Ollama não encontrado no PATH")
            break

def test_installation():
    """Testa a instalação"""
    print("🧪 Testando instalação...")
    
    try:
        # Testa importações
        import PyQt6
        import requests
        import speech_recognition
        import pyttsx3
        print("✅ Todas as bibliotecas foram importadas com sucesso")
        
        # Testa conexão com Ollama
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Conexão com Ollama funcionando")
        
        # Testa TTS
        engine = pyttsx3.init()
        print("✅ Engine TTS inicializado")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def main():
    """Função principal de setup"""
    print("🧠👑 Configuração do Cérebro Digital da Queen")
    print("=" * 50)
    
    success = True
    
    # Verificações básicas
    if not check_python_version():
        success = False
    
    # Instalação de dependências
    if success and not install_dependencies():
        success = False
    
    # Verificações de serviços
    ollama_ok = check_ollama()
    n8n_ok = check_n8n()
    
    if not ollama_ok:
        print("⚠️  Ollama não está rodando. Algumas funcionalidades podem não funcionar.")
    
    if not n8n_ok:
        print("⚠️  n8n não está rodando. Funcionalidades de workflow podem não funcionar.")
    
    # Configuração do ambiente
    create_directories()
    initialize_databases()
    create_config_file()
    
    # Download de modelos (se Ollama estiver disponível)
    if ollama_ok:
        download_models()
    
    # Teste final
    if success and test_installation():
        print("\n🎉 Configuração concluída com sucesso!")
        print("\nPara iniciar o Cérebro Digital da Queen:")
        print("  python app_queen.py")
        print("\nPara verificar o status:")
        print("  python scripts/status.py")
    else:
        print("\n❌ Configuração concluída com alguns problemas.")
        print("Verifique os erros acima e tente novamente.")
    
    print("\n📚 Documentação disponível em: docs/")
    print("🔗 Repositório: https://github.com/GabrielJaccoud/meu-cerebro-digital")

if __name__ == "__main__":
    main()

