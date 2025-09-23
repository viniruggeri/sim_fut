import yaml
import logging
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config.yaml"

# Carregar configurações do YAML
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# Configurar logging baseado nas configurações
logging.basicConfig(
    level=getattr(logging, config["logging"]["level"]),
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Configurar logging para arquivos
file_handler = logging.FileHandler(config["logging"]["file"])
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(file_handler)

logger = logging.getLogger(__name__)