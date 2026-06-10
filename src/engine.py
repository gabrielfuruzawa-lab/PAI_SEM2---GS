"""Motor de análise da Mission Control AI."""
import os
from ollama import Client
from dotenv import load_dotenv
from pathlib import Path
import src.telemetria as telemetria
import src.alertas as alertas

load_dotenv()

TRILHA = "envirosat"

client = Client(
    host="https://ollama.com",
    headers={'Authorization': f"Bearer {os.environ.get('OLLAMA_API_KEY', '')}"}
)

def llm(prompt, system=None, max_tokens=800, temperature=0.3):
    """Envia prompt ao gpt-oss:120b via Ollama Cloud."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    
    try:
        return client.chat(
            model="gpt-oss:120b", messages=messages,
            options={"num_predict": max_tokens, "temperature": temperature},
            stream=False
        )['message']['content'].strip()
    except Exception as e:
        return f"⚠️ Erro ao consultar IA: {e}"

def load_system_prompt():
    """Lê o system prompt do arquivo."""
    path = Path("prompts/system_prompt.md")
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "Você é a inteligência artificial do sistema EnviroSat."

class MissionEngine:
    def __init__(self):
        self.trilha = TRILHA
        self.system_prompt = load_system_prompt()
        self.dados_atuais = telemetria.coletar() # Linha nova: guarda o estado inicial
        
    def is_ready(self):
        return True
        
    def status_snapshot(self):
        self.dados_atuais = telemetria.coletar() # Linha alterada: gera novos dados só no /status
        dados = self.dados_atuais
        alertas_ativos = alertas.avaliar(dados)
        status = f"🌡️ Temp: {dados['sensor_termico_celsius']}°C | 🔋 Energia: {dados['energia_disponivel_pct']}% | 🛰️ GPS: {dados['precisao_geolocalizacao_m']}m"
        if alertas_ativos:
            status += "\n\n🚨 ALERTAS ATIVOS:\n" + "\n".join(alertas_ativos)
        return status

    def analyze(self, pergunta_usuario):
        dados = self.dados_atuais # Linha alterada: lê os dados congelados em vez de sortear novos
        lista_alertas = alertas.avaliar(dados)
        
        texto_alertas = "Operação normal. Sem anomalias."
        if lista_alertas:
            texto_alertas = " ".join(lista_alertas)
            
        prompt_completo = f"""
[DADOS DE TELEMETRIA SIMULADOS AGORA]
Sensores: {dados}
Diagnóstico do Sistema: {texto_alertas}

[PERGUNTA DO USUÁRIO OPERADOR]
{pergunta_usuario}
"""
        return llm(prompt_completo, system=self.system_prompt)