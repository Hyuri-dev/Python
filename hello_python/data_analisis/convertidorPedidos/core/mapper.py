from pathlib import Path
from typing import Dict, Iterable, List, Set
import pandas as pd


REQUIRED_MAP_COLUMNS = {"PRODUCTOS-SISTEMA", "COLUMNA-PLANTILLA"}


def load_product_mapping(ruta_productos: str | Path) -> Dict[str, str]:
    """
    Lee el archivo Excel de mapeo de productos y retorna un diccionario:
    {Producto del sistema -> Nombre de columna en la plantilla}.
    """
    path = Path(ruta_productos)
    if not path.is_file():
        raise FileNotFoundError(f"No se encontró el archivo de mapeo de productos: '{path}'")

    df_map = pd.read_excel(path)
    df_map.columns = df_map.columns.astype(str).str.strip()

    missing_cols = REQUIRED_MAP_COLUMNS - set(df_map.columns)
    if missing_cols:
        raise ValueError(
            f"El archivo de productos no contiene las columnas requeridas: {', '.join(sorted(missing_cols))}"
        )

    df_map = df_map.dropna(subset=["PRODUCTOS-SISTEMA", "COLUMNA-PLANTILLA"])
    productos_sistema = df_map["PRODUCTOS-SISTEMA"].astype(str).str.strip()
    columnas_plantilla = df_map["COLUMNA-PLANTILLA"].astype(str).str.strip()

    return dict(zip(productos_sistema, columnas_plantilla))


def find_unmapped_products(
    productos_pedido: Iterable[str],
    mapeo_productos: Dict[str, str],
) -> List[str]:
    """
    Compara mediante conjuntos (set) los productos presentes en el pedido
    contra las claves registradas en el diccionario de mapeo.
    Retorna la lista ordenada de productos no mapeados.
    """
    productos_en_pedido: Set[str] = {
        str(prod).strip() for prod in productos_pedido if pd.notna(prod) and str(prod).strip()
    }
    productos_mapeados: Set[str] = {str(k).strip() for k in mapeo_productos.keys()}

    no_mapeados = productos_en_pedido - productos_mapeados
    return sorted(no_mapeados)
