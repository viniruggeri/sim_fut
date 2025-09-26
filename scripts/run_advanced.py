#!/usr/bin/env python3
"""
Script de entrada para executar simulações avançadas.
Redireciona para o simulador de temporada completa.
"""

import sys
from pathlib import Path

# Adicionar src ao path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

def main():
    """Executa simulação avançada"""
    print("🏟️  SIMULADOR AVANÇADO - INICIANDO")
    print("="*50)
    
    try:
        # Importar e executar o simulador de temporada
        from scripts.run_season_simulation import main as run_season
        run_season()
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("Executando simulação alternativa...")
        
        # Fallback para execução direta
        import subprocess
        season_script = Path(__file__).parent / "run_season_simulation.py"
        result = subprocess.run([sys.executable, str(season_script)])
        return result.returncode
        
    except Exception as e:
        print(f"❌ Erro na execução: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)