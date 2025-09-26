#!/usr/bin/env python3
"""
Script de entrada para executar simulações simples.
Ponto de entrada limpo para o sistema de simulação básico.
"""
import sys
from pathlib import Path

# Adicionar src ao path para imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

def main():
    """Executa simulação simples"""
    print("🏟️  SIMULADOR SIMPLES - INICIANDO")
    print("="*50)
    
    try:
        # Importar e executar simulador simples
        from core.simple.simulator import main as run_simple_simulation
        run_simple_simulation()
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("Verifique se o módulo simple/simulator.py existe")
        return 1
    except Exception as e:
        print(f"❌ Erro na execução: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)