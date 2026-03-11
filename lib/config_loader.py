"""
Módulo para cargar configuraciones de idiomas desde archivos YAML.
"""
from pathlib import Path
import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
LANG_CONFIG_DIR = BASE_DIR / "config" / "languages"

def load_language_config(language_code: str) -> dict:
    """
    Carga la configuración de un idioma específico desde un archivo YAML.
    Args:
        language_code (str): Código del idioma (ej. "yine", "spanish")
    Returns:
        dict: Configuración del idioma
    Raises:
        FileNotFoundError: Si no se encuentra el archivo de configuración
    """
    config_path = LANG_CONFIG_DIR / f"{language_code}.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"No existe config para idioma: {language_code}")

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
