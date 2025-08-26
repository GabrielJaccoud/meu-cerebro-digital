# app_queen.py
import sys
import os
import json
import requests
import speech_recognition as sr
import pyttsx3
import sqlite3
import threading
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLineEdit, QLabel, QScrollArea, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPalette, QColor

# Configurações
OLLAMA_URL = "http://localhost:11434/api/generate"
N8N_URL = "http://localhost:5678/api/v1/workflows"

# --- Thread para tarefas em segundo plano ---
class WorkerThread(QThread):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, target_func, *args, **kwargs):
        super().__init__()
        self.target_func = target_func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            result = self.target_func(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

# --- Agente de IA (simulado) ---
class AIAgent:
    def __init__(self, db_path='queen_memory.db'):
        self.db_path = db_path
        self._init_db()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150) # Velocidade da fala
        self.engine.setProperty('volume', 0.9) # Volume

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt TEXT,
                response TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def _save_to_memory(self, prompt, response):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO memory (prompt, response) VALUES (?, ?)", (prompt, response))
        conn.commit()
        conn.close()

    def _get_from_memory(self, prompt_keywords):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        query = "SELECT response FROM memory WHERE prompt LIKE ? ORDER BY timestamp DESC LIMIT 1"
        result = cursor.execute(query, (f'%{prompt_keywords}%',)).fetchone()
        conn.close()
        return result[0] if result else None

    def process_prompt(self, prompt):
        # Simula busca na memória
        memory_response = self._get_from_memory(prompt.split()[0]) # Busca pela primeira palavra
        if memory_response:
            return f"(Da memória) {memory_response}"

        # Se não encontrou na memória, usa Ollama
        payload = {"model": "llama3", "prompt": prompt, "stream": False}
        try:
            response = requests.post(OLLAMA_URL, json=payload)
            response.raise_for_status() # Levanta exceção para erros HTTP
            ai_response = response.json()["response"]
            self._save_to_memory(prompt, ai_response) # Salva na memória
            return ai_response
        except requests.exceptions.RequestException as e:
            return f"Erro ao conectar com Ollama: {e}. Verifique se está rodando."
        except Exception as e:
            return f"Erro inesperado: {e}"

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.text_output.append("Ouvindo...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language='pt-BR')
            self.text_output.append(f"Você disse: {text}")
            return text
        except sr.UnknownValueError:
            self.text_output.append("Não entendi o áudio.")
            return ""
        except sr.RequestError as e:
            self.text_output.append(f"Erro no serviço de fala; {e}")
            return ""

    def analyze_image(self, image_path):
        # Simula análise de imagem com LLaVA (requer LLaVA rodando localmente)
        # Na prática, você enviaria a imagem para a API do LLaVA
        return f"Análise simulada da imagem {os.path.basename(image_path)}: Contém elementos visuais relevantes para o contexto da Queen."

    def transcribe_audio(self, audio_path):
        # Simula transcrição de áudio com Whisper.cpp (requer Whisper.cpp)
        # Na prática, você executaria o binário do Whisper.cpp
        return f"Transcrição simulada do áudio {os.path.basename(audio_path)}: 'Olá, Cérebro Digital!'"

    def import_to_n8n(self, workflow_json):
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(N8N_URL, data=workflow_json, headers=headers)
            response.raise_for_status()
            return f"Workflow importado com sucesso para o n8n! Status: {response.status_code}"
        except requests.exceptions.RequestException as e:
            return f"Erro ao importar workflow para o n8n: {e}. Verifique se o n8n está rodando e as credenciais."

# --- Interface Gráfica (PyQt6) ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cérebro Digital da Queen")
        self.setGeometry(100, 100, 800, 600)

        self.agent = AIAgent()
        self.is_running = True # Para o botão de emergência

        self._setup_ui()
        self._setup_dark_mode()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Área de entrada de texto
        input_layout = QHBoxLayout()
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Digite seu comando ou pergunta...")
        self.text_input.returnPressed.connect(self.process_text_input)
        input_layout.addWidget(self.text_input)

        send_button = QPushButton("Enviar")
        send_button.clicked.connect(self.process_text_input)
        input_layout.addWidget(send_button)

        main_layout.addLayout(input_layout)

        # Botões de ação
        action_layout = QHBoxLayout()
        self.mic_button = QPushButton("Microfone")
        self.mic_button.clicked.connect(self.start_listening)
        action_layout.addWidget(self.mic_button)

        self.image_button = QPushButton("Analisar Imagem")
        self.image_button.clicked.connect(self.analyze_image_action)
        action_layout.addWidget(self.image_button)

        self.transcribe_button = QPushButton("Transcrever Áudio")
        self.transcribe_button.clicked.connect(self.transcribe_audio_action)
        action_layout.addWidget(self.transcribe_button)

        self.emergency_button = QPushButton("Botão de Emergência (Parar)")
        self.emergency_button.setStyleSheet("background-color: red; color: white;")
        self.emergency_button.clicked.connect(self.toggle_emergency)
        action_layout.addWidget(self.emergency_button)

        main_layout.addLayout(action_layout)

        # Área de saída de texto (scrollable)
        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        self.text_output.setText("Bem-vinda, Queen! Como posso ajudar hoje?\n")
        main_layout.addWidget(self.text_output)

        # Seção de Geração de Workflow n8n
        workflow_group_box = self._create_workflow_section()
        main_layout.addWidget(workflow_group_box)

    def _create_workflow_section(self):
        # Esta função foi movida para o app_queen.py
        # e precisa ser implementada aqui para criar a seção de workflow
        # Exemplo simplificado:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("## Geração e Importação de Workflows n8n"))

        self.workflow_desc = QLineEdit()
        self.workflow_desc.setPlaceholderText("Descreva o workflow que deseja gerar (ex: 'enviar email de boas-vindas')")
        layout.addWidget(self.workflow_desc)

        generate_btn = QPushButton("Gerar Workflow (IA)")
        generate_btn.clicked.connect(self.generate_workflow)
        layout.addWidget(generate_btn)

        self.workflow_output = QTextEdit()
        self.workflow_output.setReadOnly(True)
        self.workflow_output.setPlaceholderText("JSON do workflow gerado aparecerá aqui...")
        layout.addWidget(self.workflow_output)

        import_btn = QPushButton("Importar para n8n Local")
        import_btn.clicked.connect(self.import_to_n8n_action)
        layout.addWidget(import_btn)

        return widget

    def generate_workflow(self):
        if not self.is_running:
            return
        desc = self.workflow_desc.text().strip()
        if not desc:
            return
        self.workflow_output.setText("Gerando workflow com IA...")
        def task():
            prompt = f"Gere um JSON válido de workflow do n8n para: {desc}. Apenas JSON."
            payload = {"model": "llama3", "prompt": prompt, "stream": False}
            try:
                response = requests.post(OLLAMA_URL, json=payload)
                raw = response.json()["response"]
                start = raw.find("{")
                end = raw.rfind("}") + 1
                return raw[start:end]
            except:
                return "{}"
        self.run_in_thread(task, self.on_workflow_done)

    def on_workflow_done(self, result):
        self.workflow_output.setText(result)

    def import_to_n8n_action(self):
        if not self.is_running:
            return
        workflow_json = self.workflow_output.toPlainText()
        if not workflow_json.strip():
            QMessageBox.warning(self, "Erro", "Gere um workflow primeiro.")
            return
        result = self.agent.import_to_n8n(workflow_json)
        QMessageBox.information(self, "Resultado", result)

    def process_text_input(self):
        if not self.is_running:
            return
        prompt = self.text_input.text()
        if not prompt:
            return
        self.text_input.clear()
        self.text_output.append(f"Você: {prompt}")
        self.run_in_thread(lambda: self.agent.process_prompt(prompt), self.on_ai_response)

    def on_ai_response(self, response):
        self.text_output.append(f"Cérebro Digital: {response}")
        self.agent.speak(response)

    def start_listening(self):
        if not self.is_running:
            return
        self.run_in_thread(self.agent.listen, self.on_voice_input)

    def on_voice_input(self, text):
        if text:
            self.text_input.setText(text)
            self.process_text_input()

    def analyze_image_action(self):
        if not self.is_running:
            return
        # Simula a seleção de arquivo de imagem
        image_path = "./sample_image.jpg" # Substitua por um QFileDialog.getOpenFileName
        self.text_output.append(f"Analisando imagem: {image_path}")
        self.run_in_thread(lambda: self.agent.analyze_image(image_path), self.on_image_analysis_done)

    def on_image_analysis_done(self, result):
        self.text_output.append(f"Análise de Imagem: {result}")
        self.agent.speak(result)

    def transcribe_audio_action(self):
        if not self.is_running:
            return
        # Simula a seleção de arquivo de áudio
        audio_path = "./sample_audio.wav" # Substitua por um QFileDialog.getOpenFileName
        self.text_output.append(f"Transcrevendo áudio: {audio_path}")
        self.run_in_thread(lambda: self.agent.transcribe_audio(audio_path), self.on_audio_transcription_done)

    def on_audio_transcription_done(self, result):
        self.text_output.append(f"Transcrição de Áudio: {result}")
        self.agent.speak(result)

    def toggle_emergency(self):
        self.is_running = not self.is_running
        if self.is_running:
            self.emergency_button.setText("Botão de Emergência (Parar)")
            self.emergency_button.setStyleSheet("background-color: red; color: white;")
            self.text_output.append("Cérebro Digital: Ativado.")
        else:
            self.emergency_button.setText("Cérebro Digital (Parado)")
            self.emergency_button.setStyleSheet("background-color: green; color: white;")
            self.text_output.append("Cérebro Digital: Desativado. Todas as operações suspensas.")

    def _setup_dark_mode(self):
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

    def run_in_thread(self, target, on_done):
        self.thread = WorkerThread(target)
        self.thread.finished.connect(on_done)
        self.thread.error.connect(lambda e: self.text_output.setText(f"Erro: {e}"))
        self.thread.start()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

