# tests/test_modules.py
"""
Testes para os módulos do Cérebro Digital da Queen
"""

import unittest
import os
import sys
import tempfile
import sqlite3
from unittest.mock import Mock, patch, MagicMock

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.auto_optimizer import PerformanceMonitor, AutoOptimizer
from modules.workflow_generator import AdvancedWorkflowGenerator, WorkflowTemplate
from modules.media_processor import ImageProcessor, AudioProcessor, MediaOrchestrator
from agents.agent_manager import AgentManager, DevelopmentAgent, MarketingAgent

class TestPerformanceMonitor(unittest.TestCase):
    """Testes para o PerformanceMonitor"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.monitor = PerformanceMonitor(self.temp_db.name)
    
    def tearDown(self):
        """Limpeza após os testes"""
        os.unlink(self.temp_db.name)
    
    def test_record_metric(self):
        """Testa gravação de métricas"""
        self.monitor.record_metric("test_metric", 5.0, "test context")
        
        # Verifica se foi gravado no banco
        conn = sqlite3.connect(self.temp_db.name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM performance_metrics WHERE metric_name = 'test_metric'")
        result = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(result)
        self.assertEqual(result[2], "test_metric")  # metric_name
        self.assertEqual(result[3], 5.0)  # metric_value
    
    def test_identify_bottlenecks(self):
        """Testa identificação de gargalos"""
        # Adiciona métricas que devem ser identificadas como gargalos
        for i in range(10):
            self.monitor.record_metric("slow_response_time", 8.0, "test")
            self.monitor.record_metric("high_error_rate", 0.2, "test")
        
        bottlenecks = self.monitor.identify_bottlenecks()
        
        # Deve identificar pelo menos um gargalo
        self.assertGreater(len(bottlenecks), 0)
        
        # Verifica se os tipos corretos foram identificados
        bottleneck_types = [b['type'] for b in bottlenecks]
        self.assertIn('high_latency', bottleneck_types)
        self.assertIn('high_error_rate', bottleneck_types)

class TestWorkflowGenerator(unittest.TestCase):
    """Testes para o AdvancedWorkflowGenerator"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.generator = AdvancedWorkflowGenerator()
    
    @patch('requests.post')
    def test_generate_from_prompt(self, mock_post):
        """Testa geração de workflow a partir de prompt"""
        # Mock da resposta da IA
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "response": '{"trigger_type": "webhook", "operations": ["send_email"], "integrations": ["gmail"]}'
        }
        mock_post.return_value = mock_response
        
        prompt = "Crie um workflow que envie email quando receber webhook"
        workflow = self.generator.generate_from_prompt(prompt)
        
        self.assertIsInstance(workflow, dict)
        self.assertIn("name", workflow)
        self.assertIn("nodes", workflow)
        self.assertIn("connections", workflow)
    
    def test_workflow_template(self):
        """Testa criação de template de workflow"""
        template = WorkflowTemplate("Test Workflow", "Workflow de teste")
        
        self.assertEqual(template.name, "Test Workflow")
        self.assertEqual(template.description, "Workflow de teste")
        self.assertEqual(len(template.nodes), 0)
        self.assertEqual(len(template.connections), 0)
    
    def test_simple_prompt_analysis(self):
        """Testa análise simples de prompt"""
        prompt = "enviar email quando receber novo lead"
        analysis = self.generator._simple_prompt_analysis(prompt)
        
        self.assertIn("trigger_type", analysis)
        self.assertIn("operations", analysis)
        self.assertIn("integrations", analysis)
        self.assertIn("send_email", analysis["operations"])
        self.assertIn("gmail", analysis["integrations"])

class TestImageProcessor(unittest.TestCase):
    """Testes para o ImageProcessor"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.processor = ImageProcessor()
    
    @patch('requests.post')
    @patch('requests.get')
    def test_generate_image(self, mock_get, mock_post):
        """Testa geração de imagem"""
        # Mock da resposta da API
        mock_post_response = Mock()
        mock_post_response.status_code = 200
        mock_post_response.json.return_value = {"image_url": "http://example.com/image.png"}
        mock_post.return_value = mock_post_response
        
        # Mock do download da imagem
        mock_get_response = Mock()
        mock_get_response.status_code = 200
        mock_get_response.content = b"fake_image_data"
        mock_get.return_value = mock_get_response
        
        with patch('os.makedirs'), patch('builtins.open', create=True) as mock_open:
            result = self.processor.generate_image("test prompt")
            
            self.assertIsNotNone(result)
            self.assertTrue(result.endswith('.png'))
    
    def test_create_placeholder_image(self):
        """Testa criação de imagem placeholder"""
        with patch('os.makedirs'), patch('PIL.Image.Image.save') as mock_save:
            result = self.processor._create_placeholder_image("test prompt", (512, 512))
            
            self.assertIsNotNone(result)
            self.assertTrue(result.endswith('.png'))
            mock_save.assert_called_once()

class TestAudioProcessor(unittest.TestCase):
    """Testes para o AudioProcessor"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        with patch('pyttsx3.init'):
            self.processor = AudioProcessor()
    
    @patch('speech_recognition.Recognizer.record')
    @patch('speech_recognition.Recognizer.recognize_google')
    @patch('speech_recognition.AudioFile')
    def test_transcribe_audio(self, mock_audio_file, mock_recognize, mock_record):
        """Testa transcrição de áudio"""
        # Mock do reconhecimento
        mock_recognize.return_value = "texto transcrito"
        mock_record.return_value = Mock()
        
        with patch('os.path.exists', return_value=True):
            result = self.processor.transcribe_audio("test.wav")
            
            self.assertIn('transcriptions', result)
            self.assertIn('google', result['transcriptions'])
            self.assertEqual(result['transcriptions']['google']['text'], "texto transcrito")
    
    def test_basic_audio_analysis(self):
        """Testa análise básica de áudio"""
        with patch('os.path.getsize', return_value=1024):
            result = self.processor._basic_audio_analysis("test.wav")
            
            self.assertIn('file_size', result)
            self.assertIn('format', result)
            self.assertEqual(result['file_size'], 1024)

class TestAgentManager(unittest.TestCase):
    """Testes para o AgentManager"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.manager = AgentManager(self.temp_db.name)
    
    def tearDown(self):
        """Limpeza após os testes"""
        os.unlink(self.temp_db.name)
    
    def test_register_agent(self):
        """Testa registro de agente"""
        initial_count = len(self.manager.agents)
        
        # Cria um agente mock
        mock_agent = Mock()
        mock_agent.profile.id = "test_agent"
        mock_agent.profile.name = "Test Agent"
        
        self.manager.register_agent(mock_agent)
        
        self.assertEqual(len(self.manager.agents), initial_count + 1)
        self.assertIn("test_agent", self.manager.agents)
    
    def test_find_best_agent(self):
        """Testa busca pelo melhor agente"""
        # Usa agente de desenvolvimento já registrado
        agent = self.manager.find_best_agent("code_generation", {})
        
        self.assertIsNotNone(agent)
        self.assertEqual(agent.profile.id, "dev_agent")
    
    def test_execute_task(self):
        """Testa execução de tarefa"""
        task = {
            "type": "code_generation",
            "data": {
                "requirements": "criar função simples",
                "language": "python"
            }
        }
        
        result = self.manager.execute_task(task)
        
        self.assertIn("success", result)
        self.assertIn("agent_used", result)
        self.assertIn("execution_time", result)

class TestDevelopmentAgent(unittest.TestCase):
    """Testes para o DevelopmentAgent"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.agent = DevelopmentAgent()
    
    def test_can_handle(self):
        """Testa capacidade de lidar com tarefas"""
        confidence = self.agent.can_handle("code_generation", {})
        self.assertGreater(confidence, 0.5)
        
        confidence = self.agent.can_handle("unknown_task", {})
        self.assertEqual(confidence, 0.0)
    
    def test_generate_code(self):
        """Testa geração de código"""
        task = {
            "type": "code_generation",
            "requirements": "criar aplicação Flask",
            "language": "python"
        }
        
        result = self.agent.execute_task(task)
        
        self.assertTrue(result["success"])
        self.assertIn("code", result)
        self.assertIn("from flask import Flask", result["code"])
    
    def test_review_code(self):
        """Testa revisão de código"""
        task = {
            "type": "code_review",
            "code": "print('hello')\nexcept:\n    pass"
        }
        
        result = self.agent.execute_task(task)
        
        self.assertTrue(result["success"])
        self.assertIn("suggestions", result)
        self.assertGreater(len(result["suggestions"]), 0)

class TestMarketingAgent(unittest.TestCase):
    """Testes para o MarketingAgent"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.agent = MarketingAgent()
    
    def test_create_content(self):
        """Testa criação de conteúdo"""
        task = {
            "type": "content_creation",
            "brief": "lançamento de produto",
            "content_type": "email"
        }
        
        result = self.agent.execute_task(task)
        
        self.assertTrue(result["success"])
        self.assertIn("content", result)
        self.assertIn("word_count", result)
        self.assertGreater(result["word_count"], 0)
    
    def test_plan_campaign(self):
        """Testa planejamento de campanha"""
        task = {
            "type": "campaign_planning",
            "objectives": ["aumentar vendas", "gerar leads"],
            "audience": "empresários",
            "budget": 5000
        }
        
        result = self.agent.execute_task(task)
        
        self.assertTrue(result["success"])
        self.assertIn("campaign_plan", result)
        self.assertIn("estimated_reach", result)

class TestIntegration(unittest.TestCase):
    """Testes de integração entre módulos"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
    
    def tearDown(self):
        """Limpeza após os testes"""
        os.unlink(self.temp_db.name)
    
    def test_full_workflow(self):
        """Testa workflow completo: geração -> otimização -> execução"""
        # 1. Gera workflow
        generator = AdvancedWorkflowGenerator()
        
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "response": '{"trigger_type": "webhook", "operations": ["ai_processing"], "integrations": ["ollama"]}'
            }
            mock_post.return_value = mock_response
            
            workflow = generator.generate_from_prompt("processar dados com IA")
        
        # 2. Otimiza workflow
        optimized_workflow = generator.optimize_workflow(workflow)
        
        # 3. Verifica se o workflow foi gerado corretamente
        self.assertIsInstance(workflow, dict)
        self.assertIsInstance(optimized_workflow, dict)
        self.assertIn("nodes", workflow)
        self.assertIn("connections", workflow)
    
    def test_agent_media_integration(self):
        """Testa integração entre agentes e processamento de mídia"""
        manager = AgentManager(self.temp_db.name)
        
        # Tarefa que envolve criação de conteúdo com mídia
        task = {
            "type": "content_creation",
            "data": {
                "brief": "criar post com imagem",
                "content_type": "social_media",
                "include_media": True
            }
        }
        
        result = manager.execute_task(task)
        
        self.assertIn("success", result)
        self.assertIn("agent_used", result)

if __name__ == '__main__':
    # Configura logging para os testes
    import logging
    logging.basicConfig(level=logging.WARNING)
    
    # Executa todos os testes
    unittest.main(verbosity=2)

