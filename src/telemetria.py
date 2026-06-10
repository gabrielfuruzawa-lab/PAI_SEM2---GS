"""Geração de dados simulados para a missão EnviroSat."""
import random

def coletar():
    """Retorna um dicionário com os dados simulados da telemetria."""
    return {
        "sensor_termico_celsius": round(random.uniform(15.0, 85.0), 1), # Normal: até 45°C. Fogo: > 60°C.
        "energia_disponivel_pct": round(random.uniform(10.0, 100.0), 1), # Normal: > 40%.
        "precisao_geolocalizacao_m": round(random.uniform(1.0, 50.0), 1), # Normal: até 15m.
        "buffer_imagens_pct": round(random.uniform(0.0, 95.0), 1) # Normal: até 80%.
    }