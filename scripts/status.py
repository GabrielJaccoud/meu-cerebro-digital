# scripts/status.py
"""
Script para verificar o status do Cérebro Digital da Queen
"""

import os
import sys
import json
import sqlite3
import requests
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

def check_system_status():
    """Verifica status geral do sistema"""
    print("🧠👑 Status do Cérebro Digital da Queen")
    print("=" * 50)
    
    status = {
        "python": check_python(),
        "dependencies": check_dependencies(),
        "ollama": check_ollama_status(),
        "n8n": check_n8n_status(),
        "databases": check_databases(),
        "files": check_files(),
        "performance": get_performance_summary()
    }
    
    return status

def check_python():
    """Verifica versão do Python"""
    version = sys.version.split()[0]
    compatible = sys.version_info >= (3, 8)
    
    print(f"🐍 Python: {version} {'✅' if compatible else '❌'}")
    
    return {
        "version": version,
        "compatible": compatible
    }

def check_dependencies():
    """Verifica dependências instaladas"""
    print("📦 Dependências:")
    
    dependencies = {
        "PyQt6": False,
        "requests": False,
        "speechrecognition": False,
        "pyttsx3": False,
        "sqlite3": False
    }
    
    for dep in dependencies:
        try:
            if dep == "speechrecognition":
                import speech_recognition
            elif dep == "sqlite3":
                import sqlite3
            else:
                __import__(dep.lower())
            dependencies[dep] = True
            print(f"  {dep}: ✅")
        except ImportError:
            print(f"  {dep}: ❌")
    
    all_ok = all(dependencies.values())
    print(f"  Status geral: {'✅' if all_ok else '❌'}")
    
    return dependencies

def check_ollama_status():
    """Verifica status do Ollama"""
    print("🤖 Ollama:")
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [model["name"] for model in models]
            
            print(f"  Status: ✅ Rodando")
            print(f"  Modelos: {', '.join(model_names) if model_names else 'Nenhum'}")
            
            # Testa geração
            test_response = requests.post("http://localhost:11434/api/generate", 
                                        json={"model": "llama3", "prompt": "test", "stream": False},
                                        timeout=10)
            
            if test_response.status_code == 200:
                print("  Teste de geração: ✅")
                generation_ok = True
            else:
                print("  Teste de geração: ❌")
                generation_ok = False
            
            return {
                "running": True,
                "models": model_names,
                "generation_ok": generation_ok
            }
        else:
            print("  Status: ❌ Não está respondendo")
            return {"running": False}
            
    except Exception as e:
        print(f"  Status: ❌ Erro: {e}")
        return {"running": False, "error": str(e)}

def check_n8n_status():
    """Verifica status do n8n"""
    print("🔄 n8n:")
    
    try:
        response = requests.get("http://localhost:5678", timeout=5)
        if response.status_code == 200:
            print("  Status: ✅ Rodando")
            
            # Tenta acessar API
            try:
                api_response = requests.get("http://localhost:5678/api/v1/workflows", timeout=5)
                api_ok = api_response.status_code in [200, 401]  # 401 é ok, significa que precisa auth
                print(f"  API: {'✅' if api_ok else '❌'}")
            except:
                api_ok = False
                print("  API: ❌")
            
            return {
                "running": True,
                "api_accessible": api_ok
            }
        else:
            print("  Status: ❌ Não está respondendo")
            return {"running": False}
            
    except Exception as e:
        print(f"  Status: ❌ Erro: {e}")
        return {"running": False, "error": str(e)}

def check_databases():
    """Verifica bancos de dados"""
    print("🗄️  Bancos de dados:")
    
    databases = {
        "queen_memory.db": False,
        "queen_performance.db": False,
        "agents.db": False
    }
    
    for db_name in databases:
        if os.path.exists(db_name):
            try:
                conn = sqlite3.connect(db_name)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                conn.close()
                
                databases[db_name] = len(tables) > 0
                print(f"  {db_name}: ✅ ({len(tables)} tabelas)")
            except Exception as e:
                print(f"  {db_name}: ❌ Erro: {e}")
        else:
            print(f"  {db_name}: ❌ Não encontrado")
    
    return databases

def check_files():
    """Verifica arquivos importantes"""
    print("📁 Arquivos:")
    
    important_files = {
        "app_queen.py": os.path.exists("app_queen.py"),
        "main.py": os.path.exists("main.py"),
        "requirements.txt": os.path.exists("requirements.txt"),
        "config.json": os.path.exists("config.json")
    }
    
    directories = {
        "modules/": os.path.exists("modules"),
        "agents/": os.path.exists("agents"),
        "workflows/": os.path.exists("workflows"),
        "docs/": os.path.exists("docs")
    }
    
    for file_name, exists in important_files.items():
        print(f"  {file_name}: {'✅' if exists else '❌'}")
    
    for dir_name, exists in directories.items():
        print(f"  {dir_name}: {'✅' if exists else '❌'}")
    
    return {**important_files, **directories}

def get_performance_summary():
    """Obtém resumo de performance"""
    print("📊 Performance:")
    
    try:
        if not os.path.exists("queen_performance.db"):
            print("  Dados: ❌ Banco não encontrado")
            return {"data_available": False}
        
        conn = sqlite3.connect("queen_performance.db")
        cursor = conn.cursor()
        
        # Métricas das últimas 24 horas
        since = datetime.now() - timedelta(hours=24)
        cursor.execute("""
            SELECT metric_name, AVG(metric_value), COUNT(*)
            FROM performance_metrics 
            WHERE timestamp > ?
            GROUP BY metric_name
        """, (since,))
        
        metrics = cursor.fetchall()
        conn.close()
        
        if metrics:
            print("  Métricas (24h):")
            for metric_name, avg_value, count in metrics:
                print(f"    {metric_name}: {avg_value:.2f} (média de {count} registros)")
        else:
            print("  Dados: ⚠️  Nenhuma métrica nas últimas 24h")
        
        return {
            "data_available": True,
            "metrics_24h": len(metrics),
            "metrics": {name: {"avg": avg, "count": count} for name, avg, count in metrics}
        }
        
    except Exception as e:
        print(f"  Erro: ❌ {e}")
        return {"data_available": False, "error": str(e)}

def get_memory_usage():
    """Obtém uso de memória dos bancos"""
    print("💾 Uso de armazenamento:")
    
    total_size = 0
    
    for db_file in ["queen_memory.db", "queen_performance.db", "agents.db"]:
        if os.path.exists(db_file):
            size = os.path.getsize(db_file)
            total_size += size
            print(f"  {db_file}: {size / 1024:.1f} KB")
    
    # Verifica diretórios de mídia
    media_dirs = ["generated_images", "generated_audio", "generated_videos", "refined_images"]
    media_size = 0
    
    for dir_name in media_dirs:
        if os.path.exists(dir_name):
            dir_size = sum(os.path.getsize(os.path.join(dir_name, f)) 
                          for f in os.listdir(dir_name) 
                          if os.path.isfile(os.path.join(dir_name, f)))
            media_size += dir_size
            if dir_size > 0:
                print(f"  {dir_name}/: {dir_size / 1024 / 1024:.1f} MB")
    
    print(f"  Total bancos: {total_size / 1024:.1f} KB")
    print(f"  Total mídia: {media_size / 1024 / 1024:.1f} MB")
    
    return {
        "database_size_kb": total_size / 1024,
        "media_size_mb": media_size / 1024 / 1024
    }

def check_recent_activity():
    """Verifica atividade recente"""
    print("🕒 Atividade recente:")
    
    try:
        if not os.path.exists("queen_memory.db"):
            print("  Nenhuma atividade registrada")
            return {"activity": False}
        
        conn = sqlite3.connect("queen_memory.db")
        cursor = conn.cursor()
        
        # Últimas interações
        cursor.execute("""
            SELECT timestamp, prompt 
            FROM memory 
            ORDER BY timestamp DESC 
            LIMIT 5
        """)
        
        recent = cursor.fetchall()
        conn.close()
        
        if recent:
            print("  Últimas interações:")
            for timestamp, prompt in recent:
                # Trunca prompt longo
                short_prompt = prompt[:50] + "..." if len(prompt) > 50 else prompt
                print(f"    {timestamp}: {short_prompt}")
        else:
            print("  Nenhuma interação registrada")
        
        return {
            "activity": len(recent) > 0,
            "recent_count": len(recent)
        }
        
    except Exception as e:
        print(f"  Erro: {e}")
        return {"activity": False, "error": str(e)}

def generate_health_score(status):
    """Gera pontuação de saúde do sistema"""
    score = 0
    max_score = 0
    
    # Python (10 pontos)
    max_score += 10
    if status["python"]["compatible"]:
        score += 10
    
    # Dependências (20 pontos)
    max_score += 20
    deps = status["dependencies"]
    if isinstance(deps, dict):
        score += sum(5 for dep_ok in deps.values() if dep_ok)
    
    # Ollama (25 pontos)
    max_score += 25
    if status["ollama"]["running"]:
        score += 15
        if status["ollama"].get("generation_ok"):
            score += 10
    
    # n8n (15 pontos)
    max_score += 15
    if status["n8n"]["running"]:
        score += 10
        if status["n8n"].get("api_accessible"):
            score += 5
    
    # Bancos de dados (15 pontos)
    max_score += 15
    dbs = status["databases"]
    if isinstance(dbs, dict):
        score += sum(5 for db_ok in dbs.values() if db_ok)
    
    # Arquivos (15 pontos)
    max_score += 15
    files = status["files"]
    if isinstance(files, dict):
        important_files = ["app_queen.py", "main.py", "requirements.txt"]
        score += sum(5 for file_name in important_files if files.get(file_name))
    
    health_percentage = (score / max_score) * 100 if max_score > 0 else 0
    
    return {
        "score": score,
        "max_score": max_score,
        "percentage": health_percentage,
        "status": "Excelente" if health_percentage >= 90 else
                 "Bom" if health_percentage >= 70 else
                 "Regular" if health_percentage >= 50 else
                 "Crítico"
    }

def main():
    """Função principal"""
    status = check_system_status()
    
    print("\n" + "=" * 50)
    
    get_memory_usage()
    print()
    check_recent_activity()
    
    print("\n" + "=" * 50)
    
    health = generate_health_score(status)
    print(f"🏥 Saúde do Sistema: {health['status']} ({health['percentage']:.1f}%)")
    print(f"   Pontuação: {health['score']}/{health['max_score']}")
    
    if health['percentage'] < 70:
        print("\n⚠️  Recomendações:")
        if not status["ollama"]["running"]:
            print("  • Inicie o Ollama: https://ollama.com")
        if not status["n8n"]["running"]:
            print("  • Inicie o n8n: docker run -d -p 5678:5678 n8nio/n8n")
        if not all(status["dependencies"].values()):
            print("  • Instale dependências: pip install -r requirements.txt")
    
    print(f"\n📅 Verificação realizada em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()

