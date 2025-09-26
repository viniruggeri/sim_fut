#!/bin/bash
set -e

# Script de entrada principal para containers Docker
# Suporte para diferentes tipos de simulação

echo "🏟️  Iniciando Simulador de Futebol..."
echo "📦 Container: $CONTAINER_TYPE"
echo "🏆 Liga: ${LEAGUE:-premier_league}"

# Configurar PYTHONPATH
export PYTHONPATH="/app/src:$PYTHONPATH"

# Determinar qual script executar baseado no tipo do container
case "${CONTAINER_TYPE:-advanced}" in
    "simple")
        echo "🎮 Modo: Simulação Simples"
        python /app/src/core/simple/simulator.py
        ;;
    "advanced")
        echo "🎮 Modo: Simulação Avançada"
        python /app/scripts/run_season_simulation.py
        ;;
    "interface")
        echo "🌐 Modo: Interface Web (Streamlit)"
        streamlit run /app/interface/app.py --server.port=8501 --server.address=0.0.0.0
        ;;
    *)
        echo "❌ Tipo de container desconhecido: $CONTAINER_TYPE"
        echo "Tipos válidos: simple, advanced, interface"
        exit 1
        ;;
esac