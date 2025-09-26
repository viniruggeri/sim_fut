#!/usr/bin/env python3
"""
Script de entrada para executar simulações simples.
Ponto de entrada limpo para o sistema de simulação básico.
"""
import sys
from pathlib import Path

# Executar o simulador diretamente
if __name__ == "__main__":
    import subprocess
    simulator_path = Path(__file__).parent.parent / "src" / "core" / "simple" / "simulator.py"
    subprocess.run([sys.executable, str(simulator_path)])