# modules/workflow_generator.py
"""
Gerador Avançado de Workflows do n8n
Cria workflows complexos baseados em prompts em linguagem natural
"""

import json
import requests
import sqlite3
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class WorkflowNode:
    """Representa um nó do workflow"""
    id: str
    name: str
    type: str
    parameters: Dict[str, Any]
    position: List[int]
    
@dataclass
class WorkflowConnection:
    """Representa uma conexão entre nós"""
    source_node: str
    target_node: str
    source_output: str = "main"
    target_input: str = "main"

class WorkflowTemplate:
    """Template base para workflows"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.nodes = []
        self.connections = []
    
    def add_node(self, node: WorkflowNode):
        """Adiciona um nó ao template"""
        self.nodes.append(node)
    
    def add_connection(self, connection: WorkflowConnection):
        """Adiciona uma conexão ao template"""
        self.connections.append(connection)
    
    def to_n8n_json(self) -> Dict:
        """Converte o template para JSON do n8n"""
        nodes = []
        connections = {}
        
        for node in self.nodes:
            n8n_node = {
                "id": node.id,
                "name": node.name,
                "type": node.type,
                "typeVersion": 1,
                "position": node.position,
                "parameters": node.parameters
            }
            nodes.append(n8n_node)
        
        # Processa conexões
        for conn in self.connections:
            if conn.source_node not in connections:
                connections[conn.source_node] = {conn.source_output: []}
            
            if conn.source_output not in connections[conn.source_node]:
                connections[conn.source_node][conn.source_output] = []
            
            connections[conn.source_node][conn.source_output].append({
                "node": conn.target_node,
                "type": conn.target_input,
                "index": 0
            })
        
        return {
            "name": self.name,
            "nodes": nodes,
            "connections": connections,
            "active": True,
            "settings": {},
            "staticData": None
        }

class AdvancedWorkflowGenerator:
    """Gerador avançado de workflows"""
    
    def __init__(self, ollama_url: str = "http://localhost:11434/api/generate"):
        self.ollama_url = ollama_url
        self.templates = self._load_templates()
        self.node_library = self._build_node_library()
    
    def _load_templates(self) -> Dict[str, WorkflowTemplate]:
        """Carrega templates pré-definidos"""
        templates = {}
        
        # Template: Email Marketing
        email_template = WorkflowTemplate(
            "Email Marketing Automation",
            "Envia emails personalizados baseados em triggers"
        )
        
        # Nó trigger
        trigger_node = WorkflowNode(
            id="trigger",
            name="Webhook Trigger",
            type="n8n-nodes-base.webhook",
            parameters={"path": "new-lead", "httpMethod": "POST"},
            position=[250, 300]
        )
        email_template.add_node(trigger_node)
        
        # Nó de processamento com IA
        ai_node = WorkflowNode(
            id="ai_processor",
            name="AI Content Generator",
            type="n8n-nodes-base.httpRequest",
            parameters={
                "url": self.ollama_url,
                "method": "POST",
                "jsonParameters": True,
                "options": {},
                "bodyParametersUi": {
                    "parameter": [
                        {"name": "model", "value": "llama3"},
                        {"name": "prompt", "value": "Gere um email de boas-vindas personalizado para {{ $json.name }}"},
                        {"name": "stream", "value": False}
                    ]
                }
            },
            position=[450, 300]
        )
        email_template.add_node(ai_node)
        
        # Nó de envio de email
        email_node = WorkflowNode(
            id="email_sender",
            name="Send Email",
            type="n8n-nodes-base.gmail",
            parameters={
                "operation": "send",
                "toEmail": "={{ $node.trigger.json.email }}",
                "subject": "Bem-vindo!",
                "message": "={{ $node.ai_processor.json.response }}"
            },
            position=[650, 300]
        )
        email_template.add_node(email_node)
        
        # Conexões
        email_template.add_connection(WorkflowConnection("trigger", "ai_processor"))
        email_template.add_connection(WorkflowConnection("ai_processor", "email_sender"))
        
        templates["email_marketing"] = email_template
        
        return templates
    
    def _build_node_library(self) -> Dict[str, Dict]:
        """Constrói biblioteca de nós disponíveis"""
        return {
            "triggers": {
                "webhook": {
                    "type": "n8n-nodes-base.webhook",
                    "description": "Recebe requisições HTTP",
                    "parameters": ["path", "httpMethod"]
                },
                "cron": {
                    "type": "n8n-nodes-base.cron",
                    "description": "Executa em horários programados",
                    "parameters": ["cronExpression"]
                },
                "email": {
                    "type": "n8n-nodes-base.emailReadImap",
                    "description": "Monitora novos emails",
                    "parameters": ["host", "port", "secure"]
                }
            },
            "ai_processing": {
                "ollama": {
                    "type": "n8n-nodes-base.httpRequest",
                    "description": "Processa com IA local (Ollama)",
                    "parameters": ["url", "method", "body"]
                },
                "openai": {
                    "type": "n8n-nodes-base.openAi",
                    "description": "Processa com OpenAI",
                    "parameters": ["operation", "prompt"]
                }
            },
            "data_storage": {
                "airtable": {
                    "type": "n8n-nodes-base.airtable",
                    "description": "Armazena dados no Airtable",
                    "parameters": ["operation", "base", "table"]
                },
                "sqlite": {
                    "type": "n8n-nodes-base.sqlite",
                    "description": "Armazena dados localmente",
                    "parameters": ["operation", "query"]
                }
            },
            "communication": {
                "gmail": {
                    "type": "n8n-nodes-base.gmail",
                    "description": "Envia emails via Gmail",
                    "parameters": ["operation", "toEmail", "subject", "message"]
                },
                "telegram": {
                    "type": "n8n-nodes-base.telegram",
                    "description": "Envia mensagens no Telegram",
                    "parameters": ["operation", "chatId", "text"]
                },
                "whatsapp": {
                    "type": "n8n-nodes-base.httpRequest",
                    "description": "Envia mensagens no WhatsApp",
                    "parameters": ["url", "method", "body"]
                }
            },
            "media": {
                "image_generation": {
                    "type": "n8n-nodes-base.httpRequest",
                    "description": "Gera imagens com IA",
                    "parameters": ["url", "method", "body"]
                },
                "file_upload": {
                    "type": "n8n-nodes-base.httpRequest",
                    "description": "Faz upload de arquivos",
                    "parameters": ["url", "method", "formData"]
                }
            }
        }
    
    def generate_from_prompt(self, prompt: str) -> Dict:
        """Gera workflow baseado em prompt em linguagem natural"""
        # Analisa o prompt para identificar intenções
        analysis = self._analyze_prompt(prompt)
        
        # Seleciona template base ou cria do zero
        if analysis.get("template_match"):
            template = self.templates[analysis["template_match"]]
            workflow = self._customize_template(template, analysis)
        else:
            workflow = self._create_from_scratch(analysis)
        
        return workflow.to_n8n_json()
    
    def _analyze_prompt(self, prompt: str) -> Dict:
        """Analisa o prompt para extrair intenções e entidades"""
        # Usa IA para analisar o prompt
        analysis_prompt = f"""
        Analise o seguinte prompt para criação de workflow e extraia:
        1. Tipo de trigger (webhook, cron, email, etc.)
        2. Operações necessárias (enviar email, salvar dados, processar com IA, etc.)
        3. Integrações necessárias (Gmail, Telegram, Airtable, etc.)
        4. Template que melhor se adequa (email_marketing, data_processing, etc.)
        
        Prompt: {prompt}
        
        Responda em JSON com as chaves: trigger_type, operations, integrations, template_match
        """
        
        try:
            response = requests.post(self.ollama_url, json={
                "model": "llama3",
                "prompt": analysis_prompt,
                "stream": False
            })
            
            if response.status_code == 200:
                ai_response = response.json()["response"]
                # Extrai JSON da resposta
                start = ai_response.find("{")
                end = ai_response.rfind("}") + 1
                if start != -1 and end > start:
                    return json.loads(ai_response[start:end])
        
        except Exception as e:
            print(f"Erro na análise do prompt: {e}")
        
        # Fallback: análise simples baseada em palavras-chave
        return self._simple_prompt_analysis(prompt)
    
    def _simple_prompt_analysis(self, prompt: str) -> Dict:
        """Análise simples baseada em palavras-chave"""
        prompt_lower = prompt.lower()
        
        analysis = {
            "trigger_type": "webhook",
            "operations": [],
            "integrations": [],
            "template_match": None
        }
        
        # Identifica trigger
        if "email" in prompt_lower and ("receber" in prompt_lower or "novo" in prompt_lower):
            analysis["trigger_type"] = "email"
        elif "horário" in prompt_lower or "agenda" in prompt_lower or "cron" in prompt_lower:
            analysis["trigger_type"] = "cron"
        
        # Identifica operações
        if "enviar email" in prompt_lower or "email" in prompt_lower:
            analysis["operations"].append("send_email")
            analysis["integrations"].append("gmail")
        
        if "telegram" in prompt_lower:
            analysis["operations"].append("send_telegram")
            analysis["integrations"].append("telegram")
        
        if "salvar" in prompt_lower or "armazenar" in prompt_lower:
            analysis["operations"].append("store_data")
            analysis["integrations"].append("airtable")
        
        if "ia" in prompt_lower or "gerar" in prompt_lower or "processar" in prompt_lower:
            analysis["operations"].append("ai_processing")
            analysis["integrations"].append("ollama")
        
        # Identifica template
        if "email" in prompt_lower and "marketing" in prompt_lower:
            analysis["template_match"] = "email_marketing"
        
        return analysis
    
    def _customize_template(self, template: WorkflowTemplate, analysis: Dict) -> WorkflowTemplate:
        """Customiza um template baseado na análise"""
        # Clona o template
        customized = WorkflowTemplate(
            f"{template.name} - Customizado",
            f"{template.description} - Personalizado via IA"
        )
        
        # Copia nós e conexões
        for node in template.nodes:
            customized.add_node(node)
        
        for conn in template.connections:
            customized.add_connection(conn)
        
        # Aplica customizações baseadas na análise
        # (implementar lógica específica de customização)
        
        return customized
    
    def _create_from_scratch(self, analysis: Dict) -> WorkflowTemplate:
        """Cria workflow do zero baseado na análise"""
        workflow = WorkflowTemplate(
            "Workflow Personalizado",
            "Criado automaticamente via IA"
        )
        
        node_id_counter = 0
        x_position = 250
        y_position = 300
        
        # Adiciona trigger
        trigger_type = analysis.get("trigger_type", "webhook")
        trigger_config = self.node_library["triggers"].get(trigger_type, 
                                                          self.node_library["triggers"]["webhook"])
        
        trigger_node = WorkflowNode(
            id=f"node_{node_id_counter}",
            name=f"Trigger - {trigger_type}",
            type=trigger_config["type"],
            parameters=self._get_default_parameters(trigger_config),
            position=[x_position, y_position]
        )
        workflow.add_node(trigger_node)
        
        previous_node_id = trigger_node.id
        node_id_counter += 1
        x_position += 200
        
        # Adiciona nós baseados nas operações
        for operation in analysis.get("operations", []):
            node_config = self._get_node_config_for_operation(operation)
            if node_config:
                node = WorkflowNode(
                    id=f"node_{node_id_counter}",
                    name=f"{operation.replace('_', ' ').title()}",
                    type=node_config["type"],
                    parameters=self._get_default_parameters(node_config),
                    position=[x_position, y_position]
                )
                workflow.add_node(node)
                
                # Conecta com o nó anterior
                workflow.add_connection(WorkflowConnection(previous_node_id, node.id))
                
                previous_node_id = node.id
                node_id_counter += 1
                x_position += 200
        
        return workflow
    
    def _get_node_config_for_operation(self, operation: str) -> Optional[Dict]:
        """Obtém configuração de nó para uma operação"""
        operation_mapping = {
            "send_email": self.node_library["communication"]["gmail"],
            "send_telegram": self.node_library["communication"]["telegram"],
            "store_data": self.node_library["data_storage"]["airtable"],
            "ai_processing": self.node_library["ai_processing"]["ollama"]
        }
        
        return operation_mapping.get(operation)
    
    def _get_default_parameters(self, node_config: Dict) -> Dict:
        """Obtém parâmetros padrão para um tipo de nó"""
        # Implementa parâmetros padrão baseados no tipo de nó
        defaults = {
            "n8n-nodes-base.webhook": {"path": "webhook", "httpMethod": "POST"},
            "n8n-nodes-base.gmail": {"operation": "send"},
            "n8n-nodes-base.httpRequest": {"method": "POST", "url": self.ollama_url}
        }
        
        return defaults.get(node_config["type"], {})
    
    def save_generated_workflow(self, workflow_json: Dict, prompt: str) -> str:
        """Salva workflow gerado para histórico"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"workflows/generated_workflow_{timestamp}.json"
        
        # Adiciona metadados
        workflow_with_meta = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "prompt": prompt,
                "generator": "AdvancedWorkflowGenerator"
            },
            "workflow": workflow_json
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(workflow_with_meta, f, indent=2, ensure_ascii=False)
        
        return filename
    
    def optimize_workflow(self, workflow_json: Dict) -> Dict:
        """Otimiza um workflow existente"""
        # Analisa o workflow para identificar oportunidades de otimização
        optimizations = []
        
        nodes = workflow_json.get("nodes", [])
        
        # Verifica se há nós que podem ser paralelizados
        sequential_nodes = self._find_sequential_nodes(workflow_json)
        if len(sequential_nodes) > 3:
            optimizations.append("parallel_processing")
        
        # Verifica se há operações repetitivas que podem ser cacheadas
        repeated_operations = self._find_repeated_operations(nodes)
        if repeated_operations:
            optimizations.append("caching")
        
        # Aplica otimizações
        optimized_workflow = workflow_json.copy()
        
        for optimization in optimizations:
            if optimization == "parallel_processing":
                optimized_workflow = self._apply_parallel_processing(optimized_workflow)
            elif optimization == "caching":
                optimized_workflow = self._apply_caching(optimized_workflow)
        
        return optimized_workflow
    
    def _find_sequential_nodes(self, workflow_json: Dict) -> List[str]:
        """Encontra nós que são executados sequencialmente"""
        # Implementa lógica para identificar nós sequenciais
        return []
    
    def _find_repeated_operations(self, nodes: List[Dict]) -> List[str]:
        """Encontra operações repetitivas"""
        # Implementa lógica para identificar operações repetidas
        return []
    
    def _apply_parallel_processing(self, workflow_json: Dict) -> Dict:
        """Aplica processamento paralelo onde possível"""
        # Implementa lógica de paralelização
        return workflow_json
    
    def _apply_caching(self, workflow_json: Dict) -> Dict:
        """Aplica cache onde apropriado"""
        # Implementa lógica de cache
        return workflow_json

# Exemplo de uso
if __name__ == "__main__":
    generator = AdvancedWorkflowGenerator()
    
    # Testa geração de workflow
    prompt = "Crie um workflow que monitore novos emails, processe o conteúdo com IA para gerar uma resposta personalizada e envie via Telegram"
    
    workflow = generator.generate_from_prompt(prompt)
    filename = generator.save_generated_workflow(workflow, prompt)
    
    print(f"Workflow gerado e salvo em: {filename}")
    print(json.dumps(workflow, indent=2))

