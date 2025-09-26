#!/usr/bin/env python3
"""
CLI principal - Wrapper para execução fácil
"""
import sys
import os
from pathlib import Path

# Adicionar src/core/cli ao path e executar CLI principal
cli_path = Path(__file__).parent / "src" / "core" / "cli"
sys.path.insert(0, str(cli_path))

if __name__ == "__main__":
    import main_cli
    sys.exit(main_cli.main())