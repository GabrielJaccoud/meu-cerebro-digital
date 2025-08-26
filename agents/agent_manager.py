# agents/agent_manager.py
"""
Gerenciador de Agentes do Cérebro Digital da Queen
Coordena múltiplos agentes especializados
"""

import json
import sqlite3
import threading
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum

class AgentStatus(Enum):
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"

@dataclass
class AgentCapability:
    """Representa uma capacidade de um agente"""
    name: str
    description: str
    input_types: List[str]
    output_types: List[str]
    confidence_level: float  # 0.0 a 1.0

@dataclass
class AgentProfile:
    """Perfil de um agente"""
    id: str
    name: str
    description: str
    capabilities: List[AgentCapability]
    status: AgentStatus
    endpoint: Optional[str] = None
    api_key: Optional[str] = None
    last_activity: Optional[datetime] = None

class BaseAgent:
    """Classe base para todos os agentes"""
    
    def __init__(self, profile: AgentProfile):
        self.profile = profile
        self.status = AgentStatus.IDLE
        self.current_task = None
        self.task_history = []
    
    def can_handle(self, task_type: str, input_data: Any) -> float:
        """Retorna confiança (0-1) de que pode executar a tarefa"""
        for capability in self.profile.capabilities:
            if task_type in capability.name.lower():
                return capability.confidence_level
        return 0.0
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Executa uma tarefa (implementar nas subclasses)"""
        raise NotImplementedError("Subclasses devem implementar execute_task")
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status atual do agente"""
        return {
            "id": self.profile.id,
            "name": self.profile.name,
            "status": self.status.value,
            "current_task": self.current_task,
            "last_activity": self.profile.last_activity.isoformat() if self.profile.last_activity else None
        }

class DevelopmentAgent(BaseAgent):
    """Agente especializado em desenvolvimento e código"""
    
    def __init__(self):
        capabilities = [
            AgentCapability(
                name="code_generation",
                description="Gera código Python, JavaScript, etc.",
                input_types=["text", "requirements"],
                output_types=["code", "files"],
                confidence_level=0.9
            ),
            AgentCapability(
                name="code_review",
                description="Revisa e otimiza código existente",
                input_types=["code", "files"],
                output_types=["suggestions", "optimized_code"],
                confidence_level=0.85
            ),
            AgentCapability(
                name="debugging",
                description="Identifica e corrige bugs",
                input_types=["code", "error_logs"],
                output_types=["fixes", "explanations"],
                confidence_level=0.8
            )
        ]
        
        profile = AgentProfile(
            id="dev_agent",
            name="Agente de Desenvolvimento",
            description="Especialista em programação e desenvolvimento de software",
            capabilities=capabilities,
            status=AgentStatus.IDLE
        )
        
        super().__init__(profile)
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Executa tarefas de desenvolvimento"""
        self.status = AgentStatus.BUSY
        self.current_task = task
        
        try:
            task_type = task.get("type", "")
            
            if "code_generation" in task_type:
                return self._generate_code(task)
            elif "code_review" in task_type:
                return self._review_code(task)
            elif "debugging" in task_type:
                return self._debug_code(task)
            else:
                return {"error": f"Tipo de tarefa não suportado: {task_type}"}
                
        finally:
            self.status = AgentStatus.IDLE
            self.current_task = None
            self.profile.last_activity = datetime.now()
    
    def _generate_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Gera código baseado nos requisitos"""
        requirements = task.get("requirements", "")
        language = task.get("language", "python")
        
        # Simula geração de código (em implementação real, usaria LLM)
        if "flask" in requirements.lower():
            code = self._generate_flask_app(requirements)
        elif "react" in requirements.lower():
            code = self._generate_react_component(requirements)
        else:
            code = self._generate_generic_code(requirements, language)
        
        return {
            "success": True,
            "code": code,
            "language": language,
            "files_created": [f"generated_code.{self._get_file_extension(language)}"]
        }
    
    def _generate_flask_app(self, requirements: str) -> str:
        """Gera aplicação Flask básica"""
        return '''from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "API do Cérebro Digital da Queen"})

@app.route('/api/process', methods=['POST'])
def process():
    data = request.get_json()
    # Processa dados aqui
    return jsonify({"result": "processado", "data": data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
'''
    
    def _generate_react_component(self, requirements: str) -> str:
        """Gera componente React básico"""
        return '''import React, { useState, useEffect } from 'react';

const QueenComponent = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        // Inicialização do componente
    }, []);

    const handleAction = async () => {
        setLoading(true);
        try {
            // Lógica da ação
            console.log('Ação executada');
        } catch (error) {
            console.error('Erro:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="queen-component">
            <h2>Cérebro Digital da Queen</h2>
            <button onClick={handleAction} disabled={loading}>
                {loading ? 'Processando...' : 'Executar'}
            </button>
            {data && <div>{JSON.stringify(data)}</div>}
        </div>
    );
};

export default QueenComponent;
'''
    
    def _generate_generic_code(self, requirements: str, language: str) -> str:
        """Gera código genérico"""
        if language.lower() == "python":
            return f'''# Código gerado para: {requirements}

def main():
    """Função principal"""
    print("Cérebro Digital da Queen - Código Gerado")
    # Implementar lógica aqui
    pass

if __name__ == "__main__":
    main()
'''
        else:
            return f"// Código gerado para: {requirements}\n// Linguagem: {language}\n\nconsole.log('Cérebro Digital da Queen');"
    
    def _get_file_extension(self, language: str) -> str:
        """Retorna extensão de arquivo para a linguagem"""
        extensions = {
            "python": "py",
            "javascript": "js",
            "typescript": "ts",
            "java": "java",
            "cpp": "cpp",
            "c": "c"
        }
        return extensions.get(language.lower(), "txt")
    
    def _review_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Revisa código existente"""
        code = task.get("code", "")
        
        suggestions = []
        
        # Análise básica do código
        if "print(" in code and "logging" not in code:
            suggestions.append("Considere usar logging em vez de print para melhor controle")
        
        if "except:" in code:
            suggestions.append("Evite except genérico, especifique o tipo de exceção")
        
        if len(code.split('\n')) > 50 and "def " not in code:
            suggestions.append("Considere dividir o código em funções menores")
        
        return {
            "success": True,
            "suggestions": suggestions,
            "code_quality_score": 0.8,  # Simulado
            "issues_found": len(suggestions)
        }
    
    def _debug_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Debug de código com erros"""
        code = task.get("code", "")
        error_message = task.get("error", "")
        
        fixes = []
        
        # Análise básica de erros comuns
        if "NameError" in error_message:
            fixes.append("Verifique se todas as variáveis estão definidas antes do uso")
        
        if "IndentationError" in error_message:
            fixes.append("Corrija a indentação do código Python")
        
        if "SyntaxError" in error_message:
            fixes.append("Verifique a sintaxe, parênteses e dois pontos")
        
        return {
            "success": True,
            "fixes": fixes,
            "error_analysis": f"Erro analisado: {error_message}",
            "confidence": 0.7
        }

class MarketingAgent(BaseAgent):
    """Agente especializado em marketing e conteúdo"""
    
    def __init__(self):
        capabilities = [
            AgentCapability(
                name="content_creation",
                description="Cria conteúdo para marketing",
                input_types=["text", "brief"],
                output_types=["content", "copy"],
                confidence_level=0.9
            ),
            AgentCapability(
                name="campaign_planning",
                description="Planeja campanhas de marketing",
                input_types=["objectives", "audience"],
                output_types=["campaign_plan", "strategy"],
                confidence_level=0.85
            )
        ]
        
        profile = AgentProfile(
            id="marketing_agent",
            name="Agente de Marketing",
            description="Especialista em marketing digital e criação de conteúdo",
            capabilities=capabilities,
            status=AgentStatus.IDLE
        )
        
        super().__init__(profile)
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Executa tarefas de marketing"""
        self.status = AgentStatus.BUSY
        self.current_task = task
        
        try:
            task_type = task.get("type", "")
            
            if "content_creation" in task_type:
                return self._create_content(task)
            elif "campaign_planning" in task_type:
                return self._plan_campaign(task)
            else:
                return {"error": f"Tipo de tarefa não suportado: {task_type}"}
                
        finally:
            self.status = AgentStatus.IDLE
            self.current_task = None
            self.profile.last_activity = datetime.now()
    
    def _create_content(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Cria conteúdo de marketing"""
        brief = task.get("brief", "")
        content_type = task.get("content_type", "post")
        
        if content_type == "email":
            content = self._create_email_content(brief)
        elif content_type == "social_media":
            content = self._create_social_media_content(brief)
        else:
            content = self._create_generic_content(brief)
        
        return {
            "success": True,
            "content": content,
            "content_type": content_type,
            "word_count": len(content.split())
        }
    
    def _create_email_content(self, brief: str) -> str:
        """Cria conteúdo para email marketing"""
        return f"""Assunto: Transforme seu negócio com IA

Olá!

Você já imaginou ter um assistente digital que nunca dorme, nunca se cansa e está sempre pronto para ajudar seu negócio a crescer?

O Cérebro Digital da Queen é exatamente isso: uma solução de inteligência artificial que revoluciona a forma como você trabalha.

✨ Principais benefícios:
• Automação inteligente de processos
• Respostas instantâneas 24/7
• Integração com suas ferramentas favoritas
• Aprendizado contínuo com suas necessidades

{brief}

Pronta para dar o próximo passo?

Com carinho,
Sua Queen Digital 👑
"""
    
    def _create_social_media_content(self, brief: str) -> str:
        """Cria conteúdo para redes sociais"""
        return f"""🧠✨ O futuro chegou e tem nome: Cérebro Digital da Queen!

Imagine ter uma assistente que:
🎯 Entende exatamente o que você precisa
🚀 Executa tarefas em segundos
💡 Aprende e evolui com você
🌟 Nunca para de trabalhar

{brief}

#InteligenciaArtificial #Automacao #Inovacao #QueenPower #TecnologiaQueTransforma

Comente 👑 se você está pronta para essa revolução!
"""
    
    def _create_generic_content(self, brief: str) -> str:
        """Cria conteúdo genérico"""
        return f"""# Cérebro Digital da Queen

{brief}

Uma solução inovadora que combina inteligência artificial, automação e a sabedoria estratégica para transformar a forma como você trabalha e vive.

Descubra o poder da tecnologia a seu favor.
"""
    
    def _plan_campaign(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Planeja campanha de marketing"""
        objectives = task.get("objectives", [])
        audience = task.get("audience", "")
        budget = task.get("budget", 0)
        
        campaign_plan = {
            "campaign_name": "Cérebro Digital da Queen - Lançamento",
            "objectives": objectives,
            "target_audience": audience,
            "budget": budget,
            "channels": ["email", "social_media", "content_marketing"],
            "timeline": "4 semanas",
            "kpis": ["conversões", "engajamento", "alcance"],
            "content_calendar": self._create_content_calendar()
        }
        
        return {
            "success": True,
            "campaign_plan": campaign_plan,
            "estimated_reach": 10000,  # Simulado
            "confidence": 0.85
        }
    
    def _create_content_calendar(self) -> List[Dict[str, str]]:
        """Cria calendário de conteúdo"""
        return [
            {"week": 1, "content": "Teaser - O que está chegando", "channel": "social_media"},
            {"week": 2, "content": "Demonstração de funcionalidades", "channel": "email"},
            {"week": 3, "content": "Casos de sucesso", "channel": "blog"},
            {"week": 4, "content": "Call to action final", "channel": "all"}
        ]

class AgentManager:
    """Gerenciador central de todos os agentes"""
    
    def __init__(self, db_path: str = 'agents.db'):
        self.db_path = db_path
        self.agents: Dict[str, BaseAgent] = {}
        self.task_queue = []
        self.running = False
        self._init_db()
        self._register_default_agents()
    
    def _init_db(self):
        """Inicializa banco de dados de agentes"""
        conn = sqlite3.connect(self.db_path)
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
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT NOT NULL,
                task_type TEXT NOT NULL,
                execution_time REAL,
                success_rate REAL,
                confidence_score REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def _register_default_agents(self):
        """Registra agentes padrão"""
        self.register_agent(DevelopmentAgent())
        self.register_agent(MarketingAgent())
    
    def register_agent(self, agent: BaseAgent):
        """Registra um novo agente"""
        self.agents[agent.profile.id] = agent
        print(f"Agente registrado: {agent.profile.name} ({agent.profile.id})")
    
    def get_available_agents(self) -> List[Dict[str, Any]]:
        """Retorna lista de agentes disponíveis"""
        return [agent.get_status() for agent in self.agents.values()]
    
    def find_best_agent(self, task_type: str, input_data: Any) -> Optional[BaseAgent]:
        """Encontra o melhor agente para uma tarefa"""
        best_agent = None
        best_confidence = 0.0
        
        for agent in self.agents.values():
            if agent.status == AgentStatus.IDLE:
                confidence = agent.can_handle(task_type, input_data)
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_agent = agent
        
        return best_agent if best_confidence > 0.5 else None
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Executa uma tarefa usando o melhor agente disponível"""
        task_type = task.get("type", "")
        input_data = task.get("data", {})
        
        # Encontra o melhor agente
        agent = self.find_best_agent(task_type, input_data)
        
        if not agent:
            return {
                "success": False,
                "error": f"Nenhum agente disponível para tarefa: {task_type}",
                "available_agents": [a.profile.name for a in self.agents.values()]
            }
        
        # Registra tarefa no banco
        task_id = self._log_task_start(agent.profile.id, task_type, task)
        
        try:
            # Executa tarefa
            start_time = datetime.now()
            result = agent.execute_task(task)
            end_time = datetime.now()
            
            execution_time = (end_time - start_time).total_seconds()
            
            # Registra resultado
            self._log_task_completion(task_id, result, execution_time)
            
            # Atualiza métricas de performance
            self._update_agent_performance(agent.profile.id, task_type, execution_time, 
                                         result.get("success", False))
            
            result["agent_used"] = agent.profile.name
            result["execution_time"] = execution_time
            
            return result
            
        except Exception as e:
            error_result = {"success": False, "error": str(e)}
            self._log_task_completion(task_id, error_result, 0)
            return error_result
    
    def _log_task_start(self, agent_id: str, task_type: str, task: Dict[str, Any]) -> int:
        """Registra início de tarefa"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO agent_tasks (agent_id, task_type, task_data, status)
            VALUES (?, ?, ?, ?)
        """, (agent_id, task_type, json.dumps(task), "running"))
        
        task_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return task_id
    
    def _log_task_completion(self, task_id: int, result: Dict[str, Any], execution_time: float):
        """Registra conclusão de tarefa"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        status = "completed" if result.get("success", False) else "failed"
        
        cursor.execute("""
            UPDATE agent_tasks 
            SET status = ?, result = ?, completed_at = ?
            WHERE id = ?
        """, (status, json.dumps(result), datetime.now(), task_id))
        
        conn.commit()
        conn.close()
    
    def _update_agent_performance(self, agent_id: str, task_type: str, 
                                execution_time: float, success: bool):
        """Atualiza métricas de performance do agente"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO agent_performance 
            (agent_id, task_type, execution_time, success_rate, confidence_score)
            VALUES (?, ?, ?, ?, ?)
        """, (agent_id, task_type, execution_time, 1.0 if success else 0.0, 0.8))
        
        conn.commit()
        conn.close()
    
    def get_agent_performance(self, agent_id: str = None) -> Dict[str, Any]:
        """Obtém métricas de performance dos agentes"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if agent_id:
            cursor.execute("""
                SELECT task_type, AVG(execution_time), AVG(success_rate), COUNT(*)
                FROM agent_performance 
                WHERE agent_id = ?
                GROUP BY task_type
            """, (agent_id,))
        else:
            cursor.execute("""
                SELECT agent_id, AVG(execution_time), AVG(success_rate), COUNT(*)
                FROM agent_performance 
                GROUP BY agent_id
            """)
        
        results = cursor.fetchall()
        conn.close()
        
        performance = {}
        for row in results:
            key = row[0]  # task_type ou agent_id
            performance[key] = {
                "avg_execution_time": row[1],
                "success_rate": row[2],
                "total_tasks": row[3]
            }
        
        return performance
    
    def generate_agent_report(self) -> str:
        """Gera relatório de status dos agentes"""
        report = "# Relatório de Agentes\n\n"
        report += f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        report += "## Agentes Registrados\n"
        for agent in self.agents.values():
            status = agent.get_status()
            report += f"- **{status['name']}** ({status['id']}): {status['status']}\n"
        
        report += "\n## Performance Geral\n"
        performance = self.get_agent_performance()
        for agent_id, metrics in performance.items():
            agent_name = self.agents.get(agent_id, {}).profile.name if agent_id in self.agents else agent_id
            report += f"- **{agent_name}**: "
            report += f"{metrics['total_tasks']} tarefas, "
            report += f"{metrics['success_rate']:.1%} sucesso, "
            report += f"{metrics['avg_execution_time']:.2f}s médio\n"
        
        return report

# Exemplo de uso
if __name__ == "__main__":
    # Inicializa gerenciador de agentes
    manager = AgentManager()
    
    # Testa execução de tarefa de desenvolvimento
    dev_task = {
        "type": "code_generation",
        "data": {
            "requirements": "Criar uma API Flask simples",
            "language": "python"
        }
    }
    
    result = manager.execute_task(dev_task)
    print("Resultado da tarefa de desenvolvimento:")
    print(json.dumps(result, indent=2))
    
    # Testa execução de tarefa de marketing
    marketing_task = {
        "type": "content_creation",
        "data": {
            "brief": "Lançamento do Cérebro Digital da Queen",
            "content_type": "email"
        }
    }
    
    result = manager.execute_task(marketing_task)
    print("\nResultado da tarefa de marketing:")
    print(json.dumps(result, indent=2))
    
    # Gera relatório
    report = manager.generate_agent_report()
    print(f"\n{report}")

