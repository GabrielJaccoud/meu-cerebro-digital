# modules/auto_optimizer.py
"""
Módulo de Auto-Otimização do Cérebro Digital da Queen
Monitora performance, identifica gargalos e otimiza automaticamente
"""

import json
import time
import sqlite3
import requests
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

class PerformanceMonitor:
    """Monitor de performance do sistema"""
    
    def __init__(self, db_path: str = 'queen_performance.db'):
        self.db_path = db_path
        self.metrics = {}
        self.running = False
        self._init_db()
    
    def _init_db(self):
        """Inicializa o banco de dados de métricas"""
        conn = sqlite3.connect(self.db_path)
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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS optimization_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                optimization_type TEXT NOT NULL,
                description TEXT,
                before_value REAL,
                after_value REAL,
                success BOOLEAN
            )
        """)
        conn.commit()
        conn.close()
    
    def record_metric(self, name: str, value: float, context: str = ""):
        """Registra uma métrica de performance"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO performance_metrics (metric_name, metric_value, context) VALUES (?, ?, ?)",
            (name, value, context)
        )
        conn.commit()
        conn.close()
        
        # Atualiza métricas em memória
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append({
            'value': value,
            'timestamp': datetime.now(),
            'context': context
        })
        
        # Mantém apenas os últimos 100 registros em memória
        if len(self.metrics[name]) > 100:
            self.metrics[name] = self.metrics[name][-100:]
    
    def get_metric_trend(self, name: str, hours: int = 24) -> List[Dict]:
        """Obtém tendência de uma métrica nas últimas horas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        since = datetime.now() - timedelta(hours=hours)
        
        cursor.execute("""
            SELECT timestamp, metric_value, context 
            FROM performance_metrics 
            WHERE metric_name = ? AND timestamp > ?
            ORDER BY timestamp DESC
        """, (name, since))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'timestamp': row[0],
                'value': row[1],
                'context': row[2]
            }
            for row in results
        ]
    
    def identify_bottlenecks(self) -> List[Dict]:
        """Identifica gargalos de performance"""
        bottlenecks = []
        
        for metric_name, values in self.metrics.items():
            if len(values) < 10:  # Precisa de dados suficientes
                continue
            
            recent_values = [v['value'] for v in values[-10:]]
            avg_recent = sum(recent_values) / len(recent_values)
            
            # Identifica métricas com valores consistentemente altos
            if metric_name.endswith('_time') and avg_recent > 5.0:  # Tempo > 5 segundos
                bottlenecks.append({
                    'type': 'high_latency',
                    'metric': metric_name,
                    'average_value': avg_recent,
                    'severity': 'high' if avg_recent > 10.0 else 'medium'
                })
            
            elif metric_name.endswith('_error_rate') and avg_recent > 0.1:  # Taxa de erro > 10%
                bottlenecks.append({
                    'type': 'high_error_rate',
                    'metric': metric_name,
                    'average_value': avg_recent,
                    'severity': 'critical' if avg_recent > 0.3 else 'high'
                })
        
        return bottlenecks

class AutoOptimizer:
    """Sistema de auto-otimização"""
    
    def __init__(self, monitor: PerformanceMonitor, ollama_url: str = "http://localhost:11434/api/generate"):
        self.monitor = monitor
        self.ollama_url = ollama_url
        self.optimization_rules = self._load_optimization_rules()
        self.running = False
    
    def _load_optimization_rules(self) -> Dict:
        """Carrega regras de otimização"""
        return {
            'high_latency': {
                'threshold': 5.0,
                'actions': ['cache_responses', 'optimize_queries', 'parallel_processing']
            },
            'high_error_rate': {
                'threshold': 0.1,
                'actions': ['retry_logic', 'fallback_models', 'error_handling']
            },
            'memory_usage': {
                'threshold': 0.8,
                'actions': ['clear_cache', 'optimize_memory', 'garbage_collection']
            }
        }
    
    def start_monitoring(self):
        """Inicia o monitoramento contínuo"""
        self.running = True
        thread = threading.Thread(target=self._monitoring_loop)
        thread.daemon = True
        thread.start()
    
    def stop_monitoring(self):
        """Para o monitoramento"""
        self.running = False
    
    def _monitoring_loop(self):
        """Loop principal de monitoramento"""
        while self.running:
            try:
                # Identifica gargalos
                bottlenecks = self.monitor.identify_bottlenecks()
                
                # Aplica otimizações se necessário
                for bottleneck in bottlenecks:
                    self._apply_optimization(bottleneck)
                
                # Aguarda antes da próxima verificação
                time.sleep(60)  # Verifica a cada minuto
                
            except Exception as e:
                print(f"Erro no loop de monitoramento: {e}")
                time.sleep(30)  # Aguarda menos tempo em caso de erro
    
    def _apply_optimization(self, bottleneck: Dict):
        """Aplica otimização baseada no gargalo identificado"""
        optimization_type = bottleneck['type']
        metric_name = bottleneck['metric']
        
        print(f"Aplicando otimização para {optimization_type} em {metric_name}")
        
        # Registra tentativa de otimização
        self._record_optimization_attempt(optimization_type, bottleneck)
        
        # Aplica otimização específica
        if optimization_type == 'high_latency':
            self._optimize_latency(bottleneck)
        elif optimization_type == 'high_error_rate':
            self._optimize_error_rate(bottleneck)
    
    def _optimize_latency(self, bottleneck: Dict):
        """Otimiza latência"""
        # Implementa cache de respostas
        # Otimiza queries
        # Implementa processamento paralelo
        pass
    
    def _optimize_error_rate(self, bottleneck: Dict):
        """Otimiza taxa de erro"""
        # Implementa lógica de retry
        # Configura modelos de fallback
        # Melhora tratamento de erros
        pass
    
    def _record_optimization_attempt(self, opt_type: str, bottleneck: Dict):
        """Registra tentativa de otimização"""
        conn = sqlite3.connect(self.monitor.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO optimization_history 
            (optimization_type, description, before_value) 
            VALUES (?, ?, ?)
        """, (
            opt_type,
            f"Otimização automática para {bottleneck['metric']}",
            bottleneck['average_value']
        ))
        conn.commit()
        conn.close()
    
    def generate_optimization_report(self) -> str:
        """Gera relatório de otimizações"""
        conn = sqlite3.connect(self.monitor.db_path)
        cursor = conn.cursor()
        
        # Últimas otimizações
        cursor.execute("""
            SELECT * FROM optimization_history 
            ORDER BY timestamp DESC LIMIT 10
        """)
        recent_optimizations = cursor.fetchall()
        
        # Métricas atuais
        bottlenecks = self.monitor.identify_bottlenecks()
        
        conn.close()
        
        report = "# Relatório de Auto-Otimização\n\n"
        report += f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        report += "## Gargalos Identificados\n"
        if bottlenecks:
            for bottleneck in bottlenecks:
                report += f"- **{bottleneck['type']}** em {bottleneck['metric']}: "
                report += f"{bottleneck['average_value']:.2f} (Severidade: {bottleneck['severity']})\n"
        else:
            report += "Nenhum gargalo crítico identificado.\n"
        
        report += "\n## Otimizações Recentes\n"
        if recent_optimizations:
            for opt in recent_optimizations:
                report += f"- **{opt[2]}**: {opt[3]} ({opt[1]})\n"
        else:
            report += "Nenhuma otimização recente.\n"
        
        return report

class WorkflowOptimizer:
    """Otimizador específico para workflows do n8n"""
    
    def __init__(self, n8n_url: str = "http://localhost:5678/api/v1"):
        self.n8n_url = n8n_url
    
    def analyze_workflow_performance(self, workflow_id: str) -> Dict:
        """Analisa performance de um workflow específico"""
        try:
            # Obtém dados de execução do workflow
            response = requests.get(f"{self.n8n_url}/executions", params={
                'workflowId': workflow_id,
                'limit': 50
            })
            
            if response.status_code == 200:
                executions = response.json()
                return self._calculate_workflow_metrics(executions)
            
        except Exception as e:
            print(f"Erro ao analisar workflow {workflow_id}: {e}")
        
        return {}
    
    def _calculate_workflow_metrics(self, executions: List[Dict]) -> Dict:
        """Calcula métricas de performance do workflow"""
        if not executions:
            return {}
        
        total_time = 0
        success_count = 0
        error_count = 0
        
        for execution in executions:
            if execution.get('finished'):
                duration = execution.get('duration', 0)
                total_time += duration
                
                if execution.get('status') == 'success':
                    success_count += 1
                else:
                    error_count += 1
        
        total_executions = len(executions)
        avg_duration = total_time / total_executions if total_executions > 0 else 0
        success_rate = success_count / total_executions if total_executions > 0 else 0
        
        return {
            'total_executions': total_executions,
            'average_duration': avg_duration,
            'success_rate': success_rate,
            'error_rate': error_count / total_executions if total_executions > 0 else 0
        }
    
    def suggest_optimizations(self, workflow_metrics: Dict) -> List[str]:
        """Sugere otimizações baseadas nas métricas"""
        suggestions = []
        
        if workflow_metrics.get('average_duration', 0) > 30:  # > 30 segundos
            suggestions.append("Considere paralelizar operações independentes")
            suggestions.append("Implemente cache para operações repetitivas")
        
        if workflow_metrics.get('error_rate', 0) > 0.1:  # > 10% de erro
            suggestions.append("Adicione tratamento de erro mais robusto")
            suggestions.append("Implemente retry automático para operações falháveis")
        
        if workflow_metrics.get('success_rate', 1) < 0.9:  # < 90% de sucesso
            suggestions.append("Revise a lógica de validação de dados")
            suggestions.append("Adicione logs detalhados para debug")
        
        return suggestions

# Exemplo de uso
if __name__ == "__main__":
    # Inicializa o sistema de monitoramento
    monitor = PerformanceMonitor()
    optimizer = AutoOptimizer(monitor)
    
    # Simula algumas métricas
    monitor.record_metric("ollama_response_time", 3.5, "phi-3 model")
    monitor.record_metric("n8n_workflow_time", 8.2, "email workflow")
    monitor.record_metric("api_error_rate", 0.15, "github api")
    
    # Inicia monitoramento
    optimizer.start_monitoring()
    
    # Gera relatório
    report = optimizer.generate_optimization_report()
    print(report)

