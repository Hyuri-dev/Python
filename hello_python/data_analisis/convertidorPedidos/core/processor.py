from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, List, Optional
import openpyxl
from openpyxl.worksheet.worksheet import Worksheet
import pandas as pd

from config.settings import DEFAULT_TEMPLATE_PATH
from core.mapper import find_unmapped_products, load_product_mapping


ProgressCallback = Callable[[float, str], None]


@dataclass
class ConversionResult:
    """Resultado estructurado del procesamiento de pedidos."""

    total_clientes: int
    no_mapeados: List[str] = field(default_factory=list)
    ruta_guardado: str = ""


class OrderProcessor:
    """Clase desacoplada para procesar pedidos y cargarlos en la plantilla Excel."""

    REQUIRED_ORDER_COLUMNS = {"Nombre Cliente", "Nombre Producto", "Cantidad Pedida"}

    @staticmethod
    def _notify(callback: Optional[ProgressCallback], progress: float, message: str) -> None:
        if callback is not None:
            callback(progress, message)

    @staticmethod
    def _resolve_output_path(ruta_salida: str | Path) -> Path:
        salida = Path(ruta_salida)
        if salida.suffix.lower() in (".xlsx", ".xlsm"):
            salida.parent.mkdir(parents=True, exist_ok=True)
            return salida
        salida.mkdir(parents=True, exist_ok=True)
        return salida / "plantilla_con_pedidos_cargados.xlsx"

    @staticmethod
    def _resolve_template_path(
        ruta_plantilla: Optional[str | Path],
        ruta_salida: str | Path,
        ruta_pedidos: str | Path,
    ) -> Path:
        candidates: List[Path] = []
        if ruta_plantilla and str(ruta_plantilla).strip():
            candidates.append(Path(str(ruta_plantilla).strip()))

        candidates.append(DEFAULT_TEMPLATE_PATH)
        candidates.append(Path(ruta_pedidos).resolve().parent / "plantilla_pedidos.xlsx")

        salida_path = Path(ruta_salida)
        if salida_path.suffix.lower() in (".xlsx", ".xlsm") and salida_path.is_file():
            candidates.append(salida_path)
        elif salida_path.is_dir():
            candidates.append(salida_path / "plantilla_pedidos.xlsx")

        for candidate in candidates:
            if candidate.is_file():
                return candidate

        raise FileNotFoundError(
            "No se encontró el archivo 'plantilla_pedidos.xlsx'. "
            "Por favor selecciónalo en la pestaña de Configuración."
        )

    def process(
        self,
        ruta_pedidos: str | Path,
        ruta_productos: str | Path,
        ruta_salida: str | Path,
        ruta_plantilla: Optional[str | Path] = None,
        progress_callback: Optional[ProgressCallback] = None,
    ) -> ConversionResult:
        """
        Ejecuta el flujo completo de conversión de pedidos sin llamadas a print():
        1. Lectura de pedidos (skiprows=9) y limpieza de nulos.
        2. Consolidación con tabla dinámica (pivot_table).
        3. Cruce con catálogo de mapeo y detección de productos no mapeados.
        4. Escritura por coordenadas en plantilla de OpenPyXL preservando fórmulas.
        5. Guardado en la ruta de salida configurada.
        """
        pedidos_path = Path(ruta_pedidos)
        if not pedidos_path.is_file():
            raise FileNotFoundError(f"No se encontró el archivo de pedidos: '{pedidos_path}'")

        # 1. LEER EL ARCHIVO DE PEDIDOS
        self._notify(progress_callback, 0.10, "Leyendo archivo de pedidos...")
        df = pd.read_excel(pedidos_path, skiprows=9)

        # Limpiamos nombres de columnas
        df.columns = df.columns.astype(str).str.strip()

        missing_cols = self.REQUIRED_ORDER_COLUMNS - set(df.columns)
        if missing_cols:
            raise ValueError(
                "El archivo de pedidos no contiene las columnas esperadas "
                f"(faltan: {', '.join(sorted(missing_cols))}). "
                "Verifica que el archivo tenga el formato estándar con encabezados en la fila 10."
            )

        # Filtramos filas válidas
        df = df.dropna(subset=["Nombre Cliente", "Nombre Producto"]).copy()
        df["Nombre Cliente"] = df["Nombre Cliente"].astype(str).str.strip()
        df["Nombre Producto"] = df["Nombre Producto"].astype(str).str.strip()
        df["Cantidad Pedida"] = pd.to_numeric(df["Cantidad Pedida"], errors="coerce").fillna(0)

        # 2. PIVOT TABLE: Consolidar pedidos por cliente
        self._notify(progress_callback, 0.30, "Consolidando pedidos por cliente (Pivot Table)...")
        if df.empty:
            pivot = pd.DataFrame(columns=["Nombre Cliente"])
        else:
            pivot = df.pivot_table(
                index="Nombre Cliente",
                columns="Nombre Producto",
                values="Cantidad Pedida",
                aggfunc="sum",
                fill_value=0,
            ).reset_index()

        # 3. DICCIONARIO DE MAPEO Y DETECCIÓN DE NO MAPEADOS
        self._notify(progress_callback, 0.50, "Validando catálogo y mapeo de productos...")
        mapeo_productos = load_product_mapping(ruta_productos)
        no_mapeados = find_unmapped_products(df["Nombre Producto"].unique(), mapeo_productos)

        # 4. ABRIR LA PLANTILLA CON OPENPYXL
        self._notify(progress_callback, 0.65, "Cargando plantilla Excel...")
        template_path = self._resolve_template_path(ruta_plantilla, ruta_salida, pedidos_path)
        wb_plantilla = openpyxl.load_workbook(template_path)
        ws: Optional[Worksheet] = wb_plantilla.active  # type: ignore[assignment]
        if ws is None:
            raise RuntimeError("No se pudo cargar la hoja activa de la plantilla Excel.")

        # Crear un mapa de {Nombre de Columna: Número de Columna} de la plantilla
        col_map = {}
        for col in range(1, ws.max_column + 1):
            val = ws.cell(row=1, column=col).value
            if val is not None:
                col_map[str(val).strip().lower()] = col

        # 5. ESCRIBIR EN LA PLANTILLA
        self._notify(progress_callback, 0.75, "Escribiendo pedidos en la plantilla...")
        fila_inicio = 2  # Los datos inician en la fila 2
        total_clientes = len(pivot)

        for i, (_, row) in enumerate(pivot.iterrows()):
            fila_actual = fila_inicio + i
            cliente_nombre = str(row["Nombre Cliente"])

            # Escribir el nombre del cliente en la Columna 8 (H)
            ws.cell(row=fila_actual, column=8, value=cliente_nombre)

            # Escribir las cantidades de cada producto
            for prod_sistema, header_plantilla in mapeo_productos.items():
                if prod_sistema in row:
                    cantidad = row[prod_sistema]
                    if pd.notna(cantidad) and float(cantidad) > 0:
                        col_idx = col_map.get(header_plantilla.strip().lower())
                        if col_idx:
                            ws.cell(row=fila_actual, column=col_idx, value=cantidad)

            if total_clientes > 0 and (i % max(1, total_clientes // 10) == 0):
                avance = 0.75 + 0.15 * ((i + 1) / total_clientes)
                self._notify(
                    progress_callback,
                    min(avance, 0.90),
                    f"Procesando clientes ({i + 1}/{total_clientes})...",
                )

        # 6. GUARDAR EL RESULTADO
        self._notify(progress_callback, 0.95, "Guardando archivo consolidado...")
        output_path = self._resolve_output_path(ruta_salida)
        wb_plantilla.save(output_path)

        self._notify(progress_callback, 1.0, "¡Conversión completada con éxito!")

        return ConversionResult(
            total_clientes=total_clientes,
            no_mapeados=no_mapeados,
            ruta_guardado=str(output_path),
        )


def procesar_pedidos(
    ruta_pedidos: str | Path,
    ruta_productos: str | Path,
    ruta_salida: str | Path,
    ruta_plantilla: Optional[str | Path] = None,
    progress_callback: Optional[ProgressCallback] = None,
) -> ConversionResult:
    """Función envoltorio principal para ejecutar el procesamiento de pedidos."""
    processor = OrderProcessor()
    return processor.process(
        ruta_pedidos=ruta_pedidos,
        ruta_productos=ruta_productos,
        ruta_salida=ruta_salida,
        ruta_plantilla=ruta_plantilla,
        progress_callback=progress_callback,
    )
