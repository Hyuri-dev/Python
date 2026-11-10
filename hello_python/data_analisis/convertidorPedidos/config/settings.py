import json
import os
from pathlib import Path
from typing import Dict, List, Tuple

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR / "config.json"
DEFAULT_TEMPLATE_PATH = BASE_DIR / "src" / "assets" / "plantilla_pedidos.xlsx"

REQUIRED_KEYS = (
    "ruta_pedidos_defecto",
    "ruta_productos",
    "ruta_salida",
)

DEFAULT_CONFIG: Dict[str, str] = {
    "ruta_pedidos_defecto": "",
    "ruta_productos": "",
    "ruta_plantilla": str(DEFAULT_TEMPLATE_PATH) if DEFAULT_TEMPLATE_PATH.exists() else "",
    "ruta_salida": "",
}


class SettingsManager:
    """Gestiona la lectura, escritura y validación de config.json."""

    def __init__(self, config_path: Path = CONFIG_FILE) -> None:
        self.config_path = Path(config_path)

    def exists(self) -> bool:
        """Verifica si el archivo config.json existe."""
        return self.config_path.exists()

    def load(self) -> Dict[str, str]:
        """Carga la configuración desde config.json o retorna valores por defecto."""
        config = DEFAULT_CONFIG.copy()
        if not self.exists():
            return config

        try:
            with open(self.config_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, dict):
                    for key in DEFAULT_CONFIG:
                        if key in data and isinstance(data[key], str):
                            config[key] = data[key].strip()
        except (json.JSONDecodeError, OSError):
            pass

        return config

    def save(self, config_data: Dict[str, str]) -> Dict[str, str]:
        """Guarda la configuración en config.json y retorna el diccionario persistido."""
        clean_config = DEFAULT_CONFIG.copy()
        for key in clean_config:
            if key in config_data and config_data[key] is not None:
                clean_config[key] = str(config_data[key]).strip()

        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as file:
            json.dump(clean_config, file, indent=4, ensure_ascii=False)

        return clean_config

    def is_configured(self) -> bool:
        """Verifica si config.json existe y tiene todas las rutas clave definidas."""
        if not self.exists():
            return False
        config = self.load()
        return all(bool(config.get(key, "").strip()) for key in REQUIRED_KEYS)

    @staticmethod
    def validate_paths(
        config_data: Dict[str, str], require_template: bool = False
    ) -> Tuple[bool, List[str]]:
        """
        Valida que las rutas requeridas no estén vacías y existan en el sistema.
        Para ruta_salida, valida que exista la carpeta (o su carpeta padre si es un archivo .xlsx).
        """
        errors: List[str] = []

        ruta_pedidos = config_data.get("ruta_pedidos_defecto", "").strip()
        ruta_productos = config_data.get("ruta_productos", "").strip()
        ruta_salida = config_data.get("ruta_salida", "").strip()
        ruta_plantilla = config_data.get("ruta_plantilla", "").strip()

        if not ruta_pedidos:
            errors.append("La ruta por defecto de pedidos es obligatoria.")
        elif not os.path.exists(ruta_pedidos):
            errors.append(f"No existe la ruta de pedidos: '{ruta_pedidos}'")

        if not ruta_productos:
            errors.append("La ruta del archivo de productos (mapeo) es obligatoria.")
        elif not os.path.isfile(ruta_productos):
            errors.append(f"No se encontró el archivo de productos: '{ruta_productos}'")

        if not ruta_salida:
            errors.append("La ruta de salida es obligatoria.")
        else:
            salida_path = Path(ruta_salida)
            if salida_path.suffix.lower() in (".xlsx", ".xlsm"):
                if not salida_path.parent.exists():
                    errors.append(
                        f"La carpeta destino para el archivo de salida no existe: '{salida_path.parent}'"
                    )
            else:
                if not salida_path.exists():
                    errors.append(f"La carpeta de salida no existe: '{ruta_salida}'")

        if require_template or ruta_plantilla:
            if not ruta_plantilla:
                errors.append("La ruta de la plantilla Excel es obligatoria.")
            elif not os.path.isfile(ruta_plantilla):
                errors.append(f"No se encontró el archivo de plantilla: '{ruta_plantilla}'")

        return len(errors) == 0, errors
