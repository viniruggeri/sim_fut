import yaml
import logging
from pathlib import Path

# Caminho correto para o config.yaml (na mesma pasta)
CONFIG_PATH = Path(__file__).parent / "config.yaml"

# Carregar configurações do YAML
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# Configurar logging baseado nas configurações
logging.basicConfig(
    level=getattr(logging, config["logging"]["level"]),
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Exportar variáveis para uso com import *
__all__ = ['config', 'logger']
