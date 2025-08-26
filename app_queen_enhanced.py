# app_queen_enhanced.py
"""
Cérebro Digital da Queen - Versão Aprimorada
Integra todos os módulos avançados e funcionalidades expandidas
"""

import sys
import os
import json
import requests
import speech_recognition as sr
import pyttsx3
import sqlite3
import threading
import subprocess
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLineEdit, QLabel, QScrollArea, QMessageBox,
    QTabWidget, QProgressBar, QComboBox, QCheckBox, QSpinBox, QFileDialog,
    QGroupBox, QGridLayout, QSlider, QListWidget, QTreeWidget, QTreeWidgetItem
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QPalette, QColor, QFont, QPixmap

# Importa módulos personalizados
from modules.auto_optimizer import PerformanceMonitor, AutoOptimizer
from modules.workflow_generator import AdvancedWorkflowGenerator
from modules.media_processor import MediaOrchestrator
from agents.agent_manager import AgentManager

# Configurações
OLLAMA_URL = "http://localhost:11434/api/generate"
N8N_URL = "http://localhost:5678/api/v1/workflows"

class EnhancedWorkerThread(QThread):
    """Thread aprimorada para tarefas em segundo plano"""
    finished = pyqtSignal(object)
    error = pyqtSignal(str)
    progress = pyqtSignal(int)
    status_update = pyqtSignal(str)

    def __init__(self, target_func, *args, **kwargs):
        super().__init__()
        self.target_func = target_func
        self.args = args
        self.kwargs = kwargs
        self.progress_callback = None
        self.status_callback = None

    def set_progress_callback(self, callback):
        """Define callback para progresso"""
        self.progress_callback = callback

    def set_status_callback(self, callback):
        """Define callback para status"""
        self.status_callback = callback

    def run(self):
        try:
            # Injeta callbacks se a função os suporta
            if self.progress_callback:
                self.kwargs['progress_callback'] = self.progress_callback
            if self.status_callback:
                self.kwargs['status_callback'] = self.status_callback
            
            result = self.target_func(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class EnhancedAIAgent:
    """Agente de IA aprimorado com todas as funcionalidades"""
    
    def __init__(self, db_path='queen_memory.db'):
        self.db_path = db_path
        self._init_db()
        
        # Inicializa componentes
        self.performance_monitor = PerformanceMonitor()
        self.auto_optimizer = AutoOptimizer(self.performance_monitor)
        self.workflow_generator = AdvancedWorkflowGenerator()
        self.media_orchestrator = MediaOrchestrator()
        self.agent_manager = AgentManager()
        
        # Configurações TTS
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        
        # Inicia monitoramento automático
        self.auto_optimizer.start_monitoring()
    
    def _init_db(self):
        """Inicializa banco de dados aprimorado"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de memória principal
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt TEXT,
                response TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                session_id TEXT,
                context TEXT,
                confidence REAL DEFAULT 0.8
            )
        """)
        
        # Tabela de conversas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                user_input TEXT,
                ai_response TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                response_time REAL,
                satisfaction_score INTEGER
            )
        """)
        
        # Tabela de preferências do usuário
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                preference_key TEXT UNIQUE,
                preference_value TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def process_prompt(self, prompt, session_id=None, progress_callback=None, status_callback=None):
        """Processa prompt com funcionalidades aprimoradas"""
        start_time = datetime.now()
        
        if status_callback:
            status_callback("Analisando prompt...")
        
        # Registra métrica de início
        self.performance_monitor.record_metric("prompt_processing_start", 1.0, prompt[:50])
        
        # Busca na memória contextual
        if status_callback:
            status_callback("Buscando contexto...")
        
        context = self._get_contextual_memory(prompt, session_id)
        
        # Determina se precisa de processamento especial
        if self._needs_agent_processing(prompt):
            if status_callback:
                status_callback("Delegando para agente especializado...")
            return self._process_with_agents(prompt, context, progress_callback, status_callback)
        
        # Processamento padrão com Ollama
        if status_callback:
            status_callback("Processando com IA...")
        
        enhanced_prompt = self._enhance_prompt_with_context(prompt, context)
        
        payload = {
            "model": "llama3",
            "prompt": enhanced_prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 2000
            }
        }
        
        try:
            response = requests.post(OLLAMA_URL, json=payload, timeout=30)
            response.raise_for_status()
            
            ai_response = response.json()["response"]
            
            # Pós-processamento
            if status_callback:
                status_callback("Finalizando resposta...")
            
            processed_response = self._post_process_response(ai_response, prompt)
            
            # Salva na memória
            self._save_enhanced_memory(prompt, processed_response, session_id, context)
            
            # Registra métricas
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds()
            self.performance_monitor.record_metric("response_time", response_time, "ollama")
            
            return processed_response
            
        except Exception as e:
            error_msg = f"Erro ao processar: {e}"
            self.performance_monitor.record_metric("error_rate", 1.0, "ollama_error")
            return error_msg
    
    def _get_contextual_memory(self, prompt, session_id):
        """Obtém memória contextual relevante"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Busca conversas recentes da sessão
        if session_id:
            cursor.execute("""
                SELECT user_input, ai_response 
                FROM conversations 
                WHERE session_id = ? 
                ORDER BY timestamp DESC 
                LIMIT 5
            """, (session_id,))
            recent_conversations = cursor.fetchall()
        else:
            recent_conversations = []
        
        # Busca memórias similares
        keywords = prompt.lower().split()[:3]  # Primeiras 3 palavras
        if keywords:
            like_pattern = f"%{keywords[0]}%"
            cursor.execute("""
                SELECT prompt, response, confidence 
                FROM memory 
                WHERE LOWER(prompt) LIKE ? 
                ORDER BY confidence DESC, timestamp DESC 
                LIMIT 3
            """, (like_pattern,))
            similar_memories = cursor.fetchall()
        else:
            similar_memories = []
        
        conn.close()
        
        return {
            "recent_conversations": recent_conversations,
            "similar_memories": similar_memories
        }
    
    def _needs_agent_processing(self, prompt):
        """Determina se o prompt precisa de processamento por agente especializado"""
        prompt_lower = prompt.lower()
        
        # Palavras-chave que indicam necessidade de agente
        agent_keywords = [
            "código", "programar", "desenvolver", "debug", "api",
            "marketing", "campanha", "conteúdo", "email", "social",
            "workflow", "n8n", "automação", "integração",
            "imagem", "gerar", "criar", "design", "visual"
        ]
        
        return any(keyword in prompt_lower for keyword in agent_keywords)
    
    def _process_with_agents(self, prompt, context, progress_callback, status_callback):
        """Processa usando sistema de agentes"""
        # Determina tipo de tarefa
        task_type = self._determine_task_type(prompt)
        
        task = {
            "type": task_type,
            "data": {
                "prompt": prompt,
                "context": context
            }
        }
        
        if progress_callback:
            progress_callback(50)
        
        result = self.agent_manager.execute_task(task)
        
        if progress_callback:
            progress_callback(100)
        
        if result.get("success"):
            return f"Tarefa executada com sucesso pelo {result.get('agent_used', 'agente')}:\n\n{result.get('content', result.get('code', str(result)))}"
        else:
            return f"Erro na execução da tarefa: {result.get('error', 'Erro desconhecido')}"
    
    def _determine_task_type(self, prompt):
        """Determina o tipo de tarefa baseado no prompt"""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ["código", "programar", "desenvolver", "debug"]):
            return "code_generation"
        elif any(word in prompt_lower for word in ["marketing", "campanha", "conteúdo", "email"]):
            return "content_creation"
        elif any(word in prompt_lower for word in ["workflow", "n8n", "automação"]):
            return "workflow_generation"
        else:
            return "general_processing"
    
    def _enhance_prompt_with_context(self, prompt, context):
        """Aprimora prompt com contexto"""
        enhanced = f"Contexto da conversa:\n"
        
        # Adiciona conversas recentes
        if context["recent_conversations"]:
            enhanced += "Conversas recentes:\n"
            for user_input, ai_response in context["recent_conversations"][-2:]:
                enhanced += f"Usuário: {user_input}\nAssistente: {ai_response}\n\n"
        
        # Adiciona memórias similares
        if context["similar_memories"]:
            enhanced += "Conhecimento relacionado:\n"
            for memory_prompt, memory_response, confidence in context["similar_memories"][:1]:
                if confidence > 0.7:
                    enhanced += f"Situação similar: {memory_prompt}\nResposta anterior: {memory_response}\n\n"
        
        enhanced += f"Pergunta atual: {prompt}\n\nResponda de forma contextualizada e personalizada:"
        
        return enhanced
    
    def _post_process_response(self, response, original_prompt):
        """Pós-processa a resposta"""
        # Remove possíveis repetições
        lines = response.split('\n')
        unique_lines = []
        for line in lines:
            if line.strip() and line not in unique_lines:
                unique_lines.append(line)
        
        processed = '\n'.join(unique_lines)
        
        # Adiciona assinatura personalizada se apropriado
        if len(processed) > 100 and not processed.endswith("Queen"):
            processed += "\n\n— Cérebro Digital da Queen 👑"
        
        return processed
    
    def _save_enhanced_memory(self, prompt, response, session_id, context):
        """Salva na memória com informações aprimoradas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Calcula confiança baseada no contexto
        confidence = 0.8
        if context["similar_memories"]:
            confidence += 0.1
        if context["recent_conversations"]:
            confidence += 0.1
        confidence = min(confidence, 1.0)
        
        cursor.execute("""
            INSERT INTO memory (prompt, response, session_id, context, confidence) 
            VALUES (?, ?, ?, ?, ?)
        """, (prompt, response, session_id, json.dumps(context), confidence))
        
        conn.commit()
        conn.close()
    
    def generate_workflow(self, description, progress_callback=None, status_callback=None):
        """Gera workflow usando o gerador avançado"""
        if status_callback:
            status_callback("Analisando descrição do workflow...")
        
        if progress_callback:
            progress_callback(25)
        
        workflow = self.workflow_generator.generate_from_prompt(description)
        
        if progress_callback:
            progress_callback(75)
        
        if status_callback:
            status_callback("Otimizando workflow...")
        
        optimized_workflow = self.workflow_generator.optimize_workflow(workflow)
        
        if progress_callback:
            progress_callback(100)
        
        # Salva workflow gerado
        filename = self.workflow_generator.save_generated_workflow(optimized_workflow, description)
        
        return {
            "workflow": optimized_workflow,
            "filename": filename,
            "description": description
        }
    
    def create_multimedia_content(self, prompt, content_type="complete", progress_callback=None, status_callback=None):
        """Cria conteúdo multimídia"""
        if status_callback:
            status_callback("Iniciando criação de conteúdo multimídia...")
        
        if progress_callback:
            progress_callback(20)
        
        content = self.media_orchestrator.create_multimedia_content(prompt, content_type)
        
        if progress_callback:
            progress_callback(100)
        
        return content
    
    def get_system_status(self):
        """Obtém status completo do sistema"""
        return {
            "performance": self.performance_monitor.identify_bottlenecks(),
            "optimization_report": self.auto_optimizer.generate_optimization_report(),
            "agent_status": self.agent_manager.get_available_agents(),
            "agent_performance": self.agent_manager.get_agent_performance()
        }

class EnhancedMainWindow(QMainWindow):
    """Interface principal aprimorada"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cérebro Digital da Queen - Versão Aprimorada")
        self.setGeometry(100, 100, 1200, 800)
        
        self.agent = EnhancedAIAgent()
        self.is_running = True
        self.current_session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        self._setup_ui()
        self._setup_dark_mode()
        self._setup_status_timer()
    
    def _setup_ui(self):
        """Configura interface aprimorada"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Cria abas
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Aba principal - Chat
        self._create_chat_tab()
        
        # Aba de workflows
        self._create_workflow_tab()
        
        # Aba de mídia
        self._create_media_tab()
        
        # Aba de agentes
        self._create_agents_tab()
        
        # Aba de configurações
        self._create_settings_tab()
        
        # Aba de status do sistema
        self._create_status_tab()
        
        # Barra de status
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Cérebro Digital da Queen - Pronto")
        
        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
    
    def _create_chat_tab(self):
        """Cria aba de chat principal"""
        chat_widget = QWidget()
        layout = QVBoxLayout(chat_widget)
        
        # Área de entrada
        input_layout = QHBoxLayout()
        
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Digite sua pergunta ou comando...")
        self.text_input.returnPressed.connect(self.process_text_input)
        input_layout.addWidget(self.text_input)
        
        send_button = QPushButton("Enviar")
        send_button.clicked.connect(self.process_text_input)
        input_layout.addWidget(send_button)
        
        layout.addLayout(input_layout)
        
        # Botões de ação
        action_layout = QHBoxLayout()
        
        self.mic_button = QPushButton("🎤 Microfone")
        self.mic_button.clicked.connect(self.start_listening)
        action_layout.addWidget(self.mic_button)
        
        self.image_button = QPushButton("🖼️ Analisar Imagem")
        self.image_button.clicked.connect(self.analyze_image_action)
        action_layout.addWidget(self.image_button)
        
        self.emergency_button = QPushButton("🛑 Emergência")
        self.emergency_button.setStyleSheet("background-color: red; color: white;")
        self.emergency_button.clicked.connect(self.toggle_emergency)
        action_layout.addWidget(self.emergency_button)
        
        layout.addLayout(action_layout)
        
        # Área de saída
        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        self.text_output.setText("🧠👑 Bem-vinda ao Cérebro Digital da Queen!\n\nComo posso ajudar hoje?\n")
        layout.addWidget(self.text_output)
        
        self.tab_widget.addTab(chat_widget, "💬 Chat")
    
    def _create_workflow_tab(self):
        """Cria aba de workflows"""
        workflow_widget = QWidget()
        layout = QVBoxLayout(workflow_widget)
        
        # Geração de workflow
        gen_group = QGroupBox("Geração de Workflow")
        gen_layout = QVBoxLayout(gen_group)
        
        self.workflow_desc = QTextEdit()
        self.workflow_desc.setPlaceholderText("Descreva o workflow que deseja criar...\nExemplo: 'Monitorar emails, processar com IA e enviar resposta no Telegram'")
        self.workflow_desc.setMaximumHeight(100)
        gen_layout.addWidget(self.workflow_desc)
        
        gen_buttons = QHBoxLayout()
        
        generate_btn = QPushButton("🧠 Gerar com IA")
        generate_btn.clicked.connect(self.generate_workflow)
        gen_buttons.addWidget(generate_btn)
        
        optimize_btn = QPushButton("⚡ Otimizar")
        optimize_btn.clicked.connect(self.optimize_workflow)
        gen_buttons.addWidget(optimize_btn)
        
        gen_layout.addLayout(gen_buttons)
        layout.addWidget(gen_group)
        
        # Visualização do workflow
        view_group = QGroupBox("Workflow Gerado")
        view_layout = QVBoxLayout(view_group)
        
        self.workflow_output = QTextEdit()
        self.workflow_output.setReadOnly(True)
        self.workflow_output.setPlaceholderText("JSON do workflow aparecerá aqui...")
        view_layout.addWidget(self.workflow_output)
        
        # Botões de ação
        action_buttons = QHBoxLayout()
        
        import_btn = QPushButton("📥 Importar para n8n")
        import_btn.clicked.connect(self.import_to_n8n_action)
        action_buttons.addWidget(import_btn)
        
        save_btn = QPushButton("💾 Salvar Arquivo")
        save_btn.clicked.connect(self.save_workflow)
        action_buttons.addWidget(save_btn)
        
        view_layout.addLayout(action_buttons)
        layout.addWidget(view_group)
        
        self.tab_widget.addTab(workflow_widget, "🔄 Workflows")
    
    def _create_media_tab(self):
        """Cria aba de mídia"""
        media_widget = QWidget()
        layout = QVBoxLayout(media_widget)
        
        # Geração de mídia
        gen_group = QGroupBox("Geração de Mídia")
        gen_layout = QGridLayout(gen_group)
        
        gen_layout.addWidget(QLabel("Prompt:"), 0, 0)
        self.media_prompt = QLineEdit()
        self.media_prompt.setPlaceholderText("Descreva o conteúdo que deseja gerar...")
        gen_layout.addWidget(self.media_prompt, 0, 1, 1, 2)
        
        gen_layout.addWidget(QLabel("Tipo:"), 1, 0)
        self.media_type = QComboBox()
        self.media_type.addItems(["Completo", "Imagem", "Áudio", "Vídeo"])
        gen_layout.addWidget(self.media_type, 1, 1)
        
        generate_media_btn = QPushButton("🎨 Gerar Mídia")
        generate_media_btn.clicked.connect(self.generate_media)
        gen_layout.addWidget(generate_media_btn, 1, 2)
        
        layout.addWidget(gen_group)
        
        # Análise de mídia
        analysis_group = QGroupBox("Análise de Mídia")
        analysis_layout = QVBoxLayout(analysis_group)
        
        file_layout = QHBoxLayout()
        self.media_file_path = QLineEdit()
        self.media_file_path.setPlaceholderText("Caminho do arquivo...")
        file_layout.addWidget(self.media_file_path)
        
        browse_btn = QPushButton("📁 Procurar")
        browse_btn.clicked.connect(self.browse_media_file)
        file_layout.addWidget(browse_btn)
        
        analyze_btn = QPushButton("🔍 Analisar")
        analyze_btn.clicked.connect(self.analyze_media_file)
        file_layout.addWidget(analyze_btn)
        
        analysis_layout.addLayout(file_layout)
        
        self.media_analysis_output = QTextEdit()
        self.media_analysis_output.setReadOnly(True)
        self.media_analysis_output.setPlaceholderText("Resultado da análise aparecerá aqui...")
        analysis_layout.addWidget(self.media_analysis_output)
        
        layout.addWidget(analysis_group)
        
        self.tab_widget.addTab(media_widget, "🎨 Mídia")
    
    def _create_agents_tab(self):
        """Cria aba de agentes"""
        agents_widget = QWidget()
        layout = QVBoxLayout(agents_widget)
        
        # Lista de agentes
        agents_group = QGroupBox("Agentes Disponíveis")
        agents_layout = QVBoxLayout(agents_group)
        
        self.agents_tree = QTreeWidget()
        self.agents_tree.setHeaderLabels(["Agente", "Status", "Última Atividade"])
        agents_layout.addWidget(self.agents_tree)
        
        refresh_agents_btn = QPushButton("🔄 Atualizar Status")
        refresh_agents_btn.clicked.connect(self.refresh_agents_status)
        agents_layout.addWidget(refresh_agents_btn)
        
        layout.addWidget(agents_group)
        
        # Execução de tarefas
        task_group = QGroupBox("Executar Tarefa")
        task_layout = QVBoxLayout(task_group)
        
        task_form = QGridLayout()
        
        task_form.addWidget(QLabel("Tipo de Tarefa:"), 0, 0)
        self.task_type = QComboBox()
        self.task_type.addItems([
            "code_generation", "code_review", "debugging",
            "content_creation", "campaign_planning",
            "workflow_generation", "media_processing"
        ])
        task_form.addWidget(self.task_type, 0, 1)
        
        task_form.addWidget(QLabel("Descrição:"), 1, 0)
        self.task_description = QTextEdit()
        self.task_description.setMaximumHeight(80)
        self.task_description.setPlaceholderText("Descreva a tarefa...")
        task_form.addWidget(self.task_description, 1, 1)
        
        execute_task_btn = QPushButton("▶️ Executar Tarefa")
        execute_task_btn.clicked.connect(self.execute_agent_task)
        task_form.addWidget(execute_task_btn, 2, 0, 1, 2)
        
        task_layout.addLayout(task_form)
        
        self.task_result = QTextEdit()
        self.task_result.setReadOnly(True)
        self.task_result.setPlaceholderText("Resultado da tarefa aparecerá aqui...")
        task_layout.addWidget(self.task_result)
        
        layout.addWidget(task_group)
        
        self.tab_widget.addTab(agents_widget, "🤖 Agentes")
    
    def _create_settings_tab(self):
        """Cria aba de configurações"""
        settings_widget = QWidget()
        layout = QVBoxLayout(settings_widget)
        
        # Configurações de IA
        ai_group = QGroupBox("Configurações de IA")
        ai_layout = QGridLayout(ai_group)
        
        ai_layout.addWidget(QLabel("Modelo Ollama:"), 0, 0)
        self.ollama_model = QComboBox()
        self.ollama_model.addItems(["llama3", "phi-3:mini", "mistral", "codellama"])
        ai_layout.addWidget(self.ollama_model, 0, 1)
        
        ai_layout.addWidget(QLabel("Temperatura:"), 1, 0)
        self.temperature_slider = QSlider(Qt.Orientation.Horizontal)
        self.temperature_slider.setRange(0, 100)
        self.temperature_slider.setValue(70)
        ai_layout.addWidget(self.temperature_slider, 1, 1)
        
        ai_layout.addWidget(QLabel("Max Tokens:"), 2, 0)
        self.max_tokens = QSpinBox()
        self.max_tokens.setRange(100, 4000)
        self.max_tokens.setValue(2000)
        ai_layout.addWidget(self.max_tokens, 2, 1)
        
        layout.addWidget(ai_group)
        
        # Configurações de TTS
        tts_group = QGroupBox("Configurações de Voz")
        tts_layout = QGridLayout(tts_group)
        
        tts_layout.addWidget(QLabel("Velocidade:"), 0, 0)
        self.tts_rate = QSlider(Qt.Orientation.Horizontal)
        self.tts_rate.setRange(50, 300)
        self.tts_rate.setValue(150)
        tts_layout.addWidget(self.tts_rate, 0, 1)
        
        tts_layout.addWidget(QLabel("Volume:"), 1, 0)
        self.tts_volume = QSlider(Qt.Orientation.Horizontal)
        self.tts_volume.setRange(0, 100)
        self.tts_volume.setValue(90)
        tts_layout.addWidget(self.tts_volume, 1, 1)
        
        self.auto_speak = QCheckBox("Falar respostas automaticamente")
        self.auto_speak.setChecked(True)
        tts_layout.addWidget(self.auto_speak, 2, 0, 1, 2)
        
        layout.addWidget(tts_group)
        
        # Configurações de interface
        ui_group = QGroupBox("Interface")
        ui_layout = QVBoxLayout(ui_group)
        
        self.dark_mode = QCheckBox("Modo escuro")
        self.dark_mode.setChecked(True)
        self.dark_mode.toggled.connect(self.toggle_theme)
        ui_layout.addWidget(self.dark_mode)
        
        self.auto_save = QCheckBox("Salvar conversas automaticamente")
        self.auto_save.setChecked(True)
        ui_layout.addWidget(self.auto_save)
        
        layout.addWidget(ui_group)
        
        # Botões de ação
        action_layout = QHBoxLayout()
        
        save_settings_btn = QPushButton("💾 Salvar Configurações")
        save_settings_btn.clicked.connect(self.save_settings)
        action_layout.addWidget(save_settings_btn)
        
        reset_settings_btn = QPushButton("🔄 Restaurar Padrões")
        reset_settings_btn.clicked.connect(self.reset_settings)
        action_layout.addWidget(reset_settings_btn)
        
        layout.addLayout(action_layout)
        
        self.tab_widget.addTab(settings_widget, "⚙️ Configurações")
    
    def _create_status_tab(self):
        """Cria aba de status do sistema"""
        status_widget = QWidget()
        layout = QVBoxLayout(status_widget)
        
        # Status dos serviços
        services_group = QGroupBox("Status dos Serviços")
        services_layout = QGridLayout(services_group)
        
        self.ollama_status = QLabel("🔴 Ollama: Verificando...")
        services_layout.addWidget(self.ollama_status, 0, 0)
        
        self.n8n_status = QLabel("🔴 n8n: Verificando...")
        services_layout.addWidget(self.n8n_status, 0, 1)
        
        self.agents_status = QLabel("🔴 Agentes: Verificando...")
        services_layout.addWidget(self.agents_status, 1, 0)
        
        self.optimizer_status = QLabel("🔴 Auto-Otimizador: Verificando...")
        services_layout.addWidget(self.optimizer_status, 1, 1)
        
        layout.addWidget(services_group)
        
        # Métricas de performance
        metrics_group = QGroupBox("Métricas de Performance")
        metrics_layout = QVBoxLayout(metrics_group)
        
        self.metrics_output = QTextEdit()
        self.metrics_output.setReadOnly(True)
        self.metrics_output.setPlaceholderText("Métricas de performance aparecerão aqui...")
        metrics_layout.addWidget(self.metrics_output)
        
        refresh_metrics_btn = QPushButton("🔄 Atualizar Métricas")
        refresh_metrics_btn.clicked.connect(self.refresh_system_metrics)
        metrics_layout.addWidget(refresh_metrics_btn)
        
        layout.addWidget(metrics_group)
        
        self.tab_widget.addTab(status_widget, "📊 Status")
    
    def _setup_dark_mode(self):
        """Configura tema escuro"""
        app = QApplication.instance()
        app.setStyle("Fusion")
        
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        
        app.setPalette(palette)
    
    def _setup_status_timer(self):
        """Configura timer para atualização de status"""
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_system_status)
        self.status_timer.start(30000)  # Atualiza a cada 30 segundos
        
        # Primeira atualização
        self.update_system_status()
    
    def process_text_input(self):
        """Processa entrada de texto com funcionalidades aprimoradas"""
        if not self.is_running:
            return
        
        prompt = self.text_input.text().strip()
        if not prompt:
            return
        
        self.text_input.clear()
        self.text_output.append(f"👤 Você: {prompt}")
        
        # Mostra barra de progresso
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Executa em thread separada
        self.run_in_thread(
            lambda: self.agent.process_prompt(prompt, self.current_session_id),
            self.on_ai_response
        )
    
    def on_ai_response(self, response):
        """Callback para resposta da IA"""
        self.text_output.append(f"🧠 Cérebro Digital: {response}")
        
        # Fala a resposta se habilitado
        if self.auto_speak.isChecked():
            self.agent.engine.say(response)
            self.agent.engine.runAndWait()
        
        # Esconde barra de progresso
        self.progress_bar.setVisible(False)
        
        # Scroll para o final
        self.text_output.verticalScrollBar().setValue(
            self.text_output.verticalScrollBar().maximum()
        )
    
    def generate_workflow(self):
        """Gera workflow usando IA"""
        description = self.workflow_desc.toPlainText().strip()
        if not description:
            QMessageBox.warning(self, "Aviso", "Digite uma descrição do workflow.")
            return
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.run_in_thread(
            lambda: self.agent.generate_workflow(description),
            self.on_workflow_generated
        )
    
    def on_workflow_generated(self, result):
        """Callback para workflow gerado"""
        self.workflow_output.setText(json.dumps(result["workflow"], indent=2))
        self.progress_bar.setVisible(False)
        
        QMessageBox.information(
            self, 
            "Sucesso", 
            f"Workflow gerado e salvo em: {result['filename']}"
        )
    
    def generate_media(self):
        """Gera conteúdo multimídia"""
        prompt = self.media_prompt.text().strip()
        if not prompt:
            QMessageBox.warning(self, "Aviso", "Digite um prompt para geração de mídia.")
            return
        
        content_type_map = {
            "Completo": "complete",
            "Imagem": "image",
            "Áudio": "audio",
            "Vídeo": "video"
        }
        
        content_type = content_type_map[self.media_type.currentText()]
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.run_in_thread(
            lambda: self.agent.create_multimedia_content(prompt, content_type),
            self.on_media_generated
        )
    
    def on_media_generated(self, content):
        """Callback para mídia gerada"""
        self.progress_bar.setVisible(False)
        
        result_text = "Conteúdo multimídia gerado:\n\n"
        for media_type, path in content.items():
            result_text += f"{media_type.title()}: {path}\n"
        
        QMessageBox.information(self, "Sucesso", result_text)
    
    def refresh_agents_status(self):
        """Atualiza status dos agentes"""
        self.agents_tree.clear()
        
        agents = self.agent.agent_manager.get_available_agents()
        
        for agent_info in agents:
            item = QTreeWidgetItem([
                agent_info["name"],
                agent_info["status"],
                agent_info.get("last_activity", "Nunca")
            ])
            self.agents_tree.addTopLevelItem(item)
    
    def execute_agent_task(self):
        """Executa tarefa usando agente"""
        task_type = self.task_type.currentText()
        description = self.task_description.toPlainText().strip()
        
        if not description:
            QMessageBox.warning(self, "Aviso", "Digite uma descrição da tarefa.")
            return
        
        task = {
            "type": task_type,
            "data": {"description": description}
        }
        
        self.progress_bar.setVisible(True)
        
        self.run_in_thread(
            lambda: self.agent.agent_manager.execute_task(task),
            self.on_agent_task_completed
        )
    
    def on_agent_task_completed(self, result):
        """Callback para tarefa de agente concluída"""
        self.progress_bar.setVisible(False)
        self.task_result.setText(json.dumps(result, indent=2))
    
    def update_system_status(self):
        """Atualiza status do sistema"""
        # Verifica Ollama
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=3)
            if response.status_code == 200:
                self.ollama_status.setText("🟢 Ollama: Online")
            else:
                self.ollama_status.setText("🟡 Ollama: Problemas")
        except:
            self.ollama_status.setText("🔴 Ollama: Offline")
        
        # Verifica n8n
        try:
            response = requests.get("http://localhost:5678", timeout=3)
            if response.status_code == 200:
                self.n8n_status.setText("🟢 n8n: Online")
            else:
                self.n8n_status.setText("🟡 n8n: Problemas")
        except:
            self.n8n_status.setText("🔴 n8n: Offline")
        
        # Status dos agentes
        agents = self.agent.agent_manager.get_available_agents()
        active_agents = len([a for a in agents if a["status"] == "idle"])
        self.agents_status.setText(f"🟢 Agentes: {active_agents} ativos")
        
        # Status do otimizador
        if self.agent.auto_optimizer.running:
            self.optimizer_status.setText("🟢 Auto-Otimizador: Ativo")
        else:
            self.optimizer_status.setText("🔴 Auto-Otimizador: Inativo")
    
    def refresh_system_metrics(self):
        """Atualiza métricas do sistema"""
        status = self.agent.get_system_status()
        
        metrics_text = "=== MÉTRICAS DE PERFORMANCE ===\n\n"
        
        # Gargalos identificados
        bottlenecks = status["performance"]
        if bottlenecks:
            metrics_text += "Gargalos Identificados:\n"
            for bottleneck in bottlenecks:
                metrics_text += f"- {bottleneck['type']}: {bottleneck['metric']} ({bottleneck['severity']})\n"
        else:
            metrics_text += "✅ Nenhum gargalo crítico identificado\n"
        
        metrics_text += "\n=== PERFORMANCE DOS AGENTES ===\n\n"
        
        # Performance dos agentes
        agent_perf = status["agent_performance"]
        for agent_id, metrics in agent_perf.items():
            agent_name = agent_id.replace("_", " ").title()
            metrics_text += f"{agent_name}:\n"
            metrics_text += f"  Tarefas: {metrics['total_tasks']}\n"
            metrics_text += f"  Taxa de sucesso: {metrics['success_rate']:.1%}\n"
            metrics_text += f"  Tempo médio: {metrics['avg_execution_time']:.2f}s\n\n"
        
        self.metrics_output.setText(metrics_text)
    
    def run_in_thread(self, target, on_done):
        """Executa função em thread separada"""
        self.thread = EnhancedWorkerThread(target)
        self.thread.finished.connect(on_done)
        self.thread.error.connect(lambda e: QMessageBox.critical(self, "Erro", str(e)))
        self.thread.progress.connect(self.progress_bar.setValue)
        self.thread.status_update.connect(self.status_bar.showMessage)
        self.thread.start()
    
    # Métodos adicionais (implementar conforme necessário)
    def start_listening(self):
        """Inicia escuta por voz"""
        pass
    
    def analyze_image_action(self):
        """Analisa imagem"""
        pass
    
    def toggle_emergency(self):
        """Alterna modo de emergência"""
        self.is_running = not self.is_running
        if self.is_running:
            self.emergency_button.setText("🛑 Emergência")
            self.emergency_button.setStyleSheet("background-color: red; color: white;")
            self.status_bar.showMessage("Sistema ativado")
        else:
            self.emergency_button.setText("▶️ Reativar")
            self.emergency_button.setStyleSheet("background-color: green; color: white;")
            self.status_bar.showMessage("Sistema pausado - Modo de emergência")
    
    def optimize_workflow(self):
        """Otimiza workflow atual"""
        pass
    
    def import_to_n8n_action(self):
        """Importa workflow para n8n"""
        pass
    
    def save_workflow(self):
        """Salva workflow em arquivo"""
        pass
    
    def browse_media_file(self):
        """Procura arquivo de mídia"""
        pass
    
    def analyze_media_file(self):
        """Analisa arquivo de mídia"""
        pass
    
    def save_settings(self):
        """Salva configurações"""
        pass
    
    def reset_settings(self):
        """Restaura configurações padrão"""
        pass
    
    def toggle_theme(self):
        """Alterna tema"""
        pass

def main():
    """Função principal"""
    app = QApplication(sys.argv)
    
    # Configura fonte
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = EnhancedMainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

