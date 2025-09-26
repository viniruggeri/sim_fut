#!/usr/bin/env python3
"""
Script de entrada para processamento de dados FIFA 25.
Converte CSV do FIFA 25 em JSONs das ligas processadas.
"""
import sys
from pathlib import Path

# Adicionar src ao path para imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Executar o arquivo diretamente
if __name__ == "__main__":
    import subprocess
    data_processor_path = Path(__file__).parent.parent / "src" / "core" / "data_processor.py"
    subprocess.run([sys.executable, str(data_processor_path)])