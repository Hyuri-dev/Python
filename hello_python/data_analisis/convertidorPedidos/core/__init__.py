"""Núcleo de procesamiento de datos y mapeo de productos."""

from core.mapper import find_unmapped_products, load_product_mapping
from core.processor import ConversionResult, OrderProcessor, procesar_pedidos

__all__ = [
    "ConversionResult",
    "OrderProcessor",
    "procesar_pedidos",
    "load_product_mapping",
    "find_unmapped_products",
]
