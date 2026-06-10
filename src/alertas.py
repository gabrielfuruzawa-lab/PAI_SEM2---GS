"""Regras de threshold e alertas para o EnviroSat."""

def avaliar(dados):
    """Avalia os dados da telemetria e retorna uma lista de alertas críticos."""
    alertas = []

    # Regra 1: Detecção de foco de incêndio (Sustentabilidade)
    if dados.get("sensor_termico_celsius", 0) > 60.0:
        alertas.append("CRÍTICO: Possível foco de incêndio detectado (Temperatura > 60°C).")

    # Regra 2: Bateria do satélite acabando
    if dados.get("energia_disponivel_pct", 100) < 20.0:
        alertas.append("ALERTA: Nível de energia crítico (< 20%). Ativar modo de economia.")

    # Regra 3: Falha de posicionamento
    if dados.get("precisao_geolocalizacao_m", 0) > 30.0:
        alertas.append("AVISO: Degradação severa na precisão do GPS (> 30m).")

    return alertas