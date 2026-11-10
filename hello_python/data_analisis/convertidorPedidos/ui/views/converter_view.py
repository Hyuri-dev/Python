import os
from pathlib import Path
import threading
from typing import Callable, Optional
import flet as ft

from config.settings import SettingsManager
from core.processor import ConversionResult, procesar_pedidos
from ui.components.file_selector import Colors, FileSelector, Icons, show_snackbar


class ConverterView(ft.Container):
    """
    Vista principal del Conversor de Pedidos:
    - Selector de archivo puntual de pedidos (precargado desde config.json).
    - Botón de inicio de conversión.
    - Barra de estado y progreso (ProgressBar + ProgressRing).
    - Notificación SnackBar y resumen del procesamiento.
    - Panel interactivo de alertas para productos no mapeados.
    """

    def __init__(
        self,
        page: ft.Page,
        settings_manager: SettingsManager,
        on_open_settings: Optional[Callable[[], None]] = None,
    ) -> None:
        super().__init__(expand=True, padding=24)
        self.host_page = page
        self.settings_manager = settings_manager
        self.on_open_settings = on_open_settings

        config = self.settings_manager.load()
        default_pedidos = self._resolve_default_order_file(
            config.get("ruta_pedidos_defecto", "")
        )

        self.pedidos_selector = FileSelector(
            page=self.host_page,
            label="Archivo de pedidos del día (.xlsx)",
            value=default_pedidos,
            hint_text="Selecciona el archivo pedidos.xlsx a procesar...",
            mode="file",
            allowed_extensions=["xlsx", "xlsm", "xls"],
        )

        self.convert_button = ft.ElevatedButton(
            text="Iniciar Conversión",
            icon=Icons.PLAY_ARROW_ROUNDED,
            style=ft.ButtonStyle(
                bgcolor=Colors.BLUE_700,
                color=Colors.WHITE,
                padding=ft.padding.symmetric(horizontal=24, vertical=16),
            ),
            on_click=self._start_conversion,
        )

        self.progress_ring = ft.ProgressRing(width=22, height=22, stroke_width=3, visible=False)
        self.status_text = ft.Text(
            "Listo para procesar pedidos.",
            size=14,
            color=Colors.GREY_700,
        )
        self.progress_bar = ft.ProgressBar(
            value=0,
            visible=False,
            color=Colors.BLUE_700,
            bgcolor=Colors.BLUE_100,
            border_radius=4,
        )

        self.summary_banner = ft.Container(
            visible=False,
            padding=14,
            border_radius=10,
            bgcolor=Colors.GREEN_50,
            border=ft.border.all(1, Colors.GREEN_400),
            content=ft.Row(
                controls=[
                    ft.Icon(Icons.CHECK_CIRCLE_OUTLINE, color=Colors.GREEN_700),
                    ft.Text("", expand=True, weight=ft.FontWeight.W_500, color=Colors.GREEN_900),
                ]
            ),
        )
        self.summary_text: ft.Text = self.summary_banner.content.controls[1]  # type: ignore[index]

        self.alerts_list = ft.ListView(
            expand=True,
            spacing=6,
            padding=8,
            auto_scroll=False,
        )

        self.alerts_header_text = ft.Text(
            "Panel de Alertas (Productos no mapeados)",
            size=16,
            weight=ft.FontWeight.BOLD,
        )
        self.alerts_badge = ft.Container(
            padding=ft.padding.symmetric(horizontal=10, vertical=4),
            border_radius=12,
            bgcolor=Colors.GREY_200,
            content=ft.Text("Sin alertas", size=12, weight=ft.FontWeight.W_600),
        )

        self.alerts_panel = ft.Container(
            expand=True,
            padding=16,
            border_radius=12,
            border=ft.border.all(1, Colors.GREY_300),
            bgcolor=Colors.SURFACE_VARIANT if hasattr(Colors, "SURFACE_VARIANT") else Colors.GREY_50,
            content=ft.Column(
                expand=True,
                spacing=10,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(
                                spacing=8,
                                controls=[
                                    ft.Icon(Icons.WARNING_AMBER_ROUNDED, color=Colors.ORANGE_700),
                                    self.alerts_header_text,
                                ],
                            ),
                            self.alerts_badge,
                        ],
                    ),
                    ft.Divider(height=1),
                    ft.Text(
                        "Aquí se mostrarán los productos presentes en el pedido que no estén registrados en el archivo de mapeo.",
                        size=13,
                        color=Colors.GREY_700,
                    ),
                    self.alerts_list,
                ],
            ),
        )

        self.content = ft.Column(
            expand=True,
            spacing=18,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column(
                            spacing=2,
                            controls=[
                                ft.Text(
                                    "Conversor de Pedidos a Plantilla",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    "Consolida pedidos por cliente y escríbelos en la plantilla preservando fórmulas.",
                                    size=14,
                                    color=Colors.GREY_700,
                                ),
                            ],
                        ),
                    ],
                ),
                ft.Divider(height=1),
                ft.Container(
                    padding=16,
                    border_radius=12,
                    border=ft.border.all(1, Colors.GREY_300),
                    content=ft.Column(
                        spacing=14,
                        controls=[
                            self.pedidos_selector,
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Row(
                                        spacing=10,
                                        controls=[
                                            self.progress_ring,
                                            self.status_text,
                                        ],
                                    ),
                                    self.convert_button,
                                ],
                            ),
                            self.progress_bar,
                        ],
                    ),
                ),
                self.summary_banner,
                self.alerts_panel,
            ],
        )

    @staticmethod
    def _resolve_default_order_file(ruta_pedidos_defecto: str) -> str:
        ruta = ruta_pedidos_defecto.strip()
        if not ruta:
            return ""
        path = Path(ruta)
        if path.is_file():
            return str(path)
        if path.is_dir():
            candidate = path / "pedidos.xlsx"
            if candidate.is_file():
                return str(candidate)
        return ruta

    def refresh_from_settings(self) -> None:
        """Actualiza la ruta precargada cuando se modifican los ajustes."""
        config = self.settings_manager.load()
        if not self.pedidos_selector.value or not os.path.isfile(self.pedidos_selector.value):
            self.pedidos_selector.value = self._resolve_default_order_file(
                config.get("ruta_pedidos_defecto", "")
            )
            self.host_page.update()

    def _start_conversion(self, _: ft.ControlEvent) -> None:
        ruta_pedidos = self.pedidos_selector.value
        if not ruta_pedidos or not os.path.isfile(ruta_pedidos):
            self.pedidos_selector.set_error(
                "Selecciona un archivo de pedidos válido (.xlsx) antes de continuar."
            )
            show_snackbar(
                self.host_page,
                "⚠️ Selecciona un archivo de pedidos válido para iniciar la conversión.",
                bgcolor=Colors.RED_700,
            )
            self.host_page.update()
            return

        config = self.settings_manager.load()
        is_valid, errors = self.settings_manager.validate_paths(
            {
                **config,
                "ruta_pedidos_defecto": ruta_pedidos,
            }
        )
        if not is_valid:
            show_snackbar(
                self.host_page,
                f"⚠️ Configuración incompleta: {errors[0]}",
                bgcolor=Colors.RED_700,
            )
            if self.on_open_settings:
                self.on_open_settings()
            return

        self.convert_button.disabled = True
        self.progress_ring.visible = True
        self.progress_bar.visible = True
        self.progress_bar.value = 0.05
        self.summary_banner.visible = False
        self.status_text.value = "Iniciando conversión..."
        self.host_page.update()

        thread = threading.Thread(
            target=self._run_conversion_worker,
            args=(
                ruta_pedidos,
                config.get("ruta_productos", ""),
                config.get("ruta_salida", ""),
                config.get("ruta_plantilla", ""),
            ),
            daemon=True,
        )
        thread.start()

    def _update_progress(self, progress: float, message: str) -> None:
        self.progress_bar.value = progress
        self.status_text.value = message
        self.host_page.update()

    def _run_conversion_worker(
        self,
        ruta_pedidos: str,
        ruta_productos: str,
        ruta_salida: str,
        ruta_plantilla: str,
    ) -> None:
        try:
            result = procesar_pedidos(
                ruta_pedidos=ruta_pedidos,
                ruta_productos=ruta_productos,
                ruta_salida=ruta_salida,
                ruta_plantilla=ruta_plantilla or None,
                progress_callback=self._update_progress,
            )
            self._on_conversion_success(result)
        except Exception as exc:
            self._on_conversion_error(str(exc))

    def _on_conversion_success(self, result: ConversionResult) -> None:
        self.convert_button.disabled = False
        self.progress_ring.visible = False
        self.progress_bar.value = 1.0

        mensaje_exito = (
            f"¡Listo! Se procesaron {result.total_clientes} clientes y se guardó en "
            f"'{result.ruta_guardado}' sin afectar fórmulas."
        )
        self.status_text.value = "Proceso finalizado."
        self.summary_text.value = mensaje_exito
        self.summary_banner.visible = True

        self._populate_alerts(result.no_mapeados)
        show_snackbar(self.host_page, mensaje_exito, bgcolor=Colors.GREEN_700)
        self.host_page.update()

    def _on_conversion_error(self, error_msg: str) -> None:
        self.convert_button.disabled = False
        self.progress_ring.visible = False
        self.progress_bar.visible = False
        self.status_text.value = f"Error: {error_msg}"
        show_snackbar(
            self.host_page,
            f"❌ Error durante el procesamiento: {error_msg}",
            bgcolor=Colors.RED_700,
        )
        self.host_page.update()

    def _populate_alerts(self, no_mapeados: list[str]) -> None:
        self.alerts_list.controls.clear()

        if not no_mapeados:
            self.alerts_badge.bgcolor = Colors.GREEN_100
            self.alerts_badge.content = ft.Text(
                "0 omitidos", size=12, weight=ft.FontWeight.W_600, color=Colors.GREEN_800
            )
            self.alerts_list.controls.append(
                ft.Container(
                    padding=12,
                    border_radius=8,
                    bgcolor=Colors.GREEN_50,
                    content=ft.Row(
                        controls=[
                            ft.Icon(Icons.VERIFIED_OUTLINED, color=Colors.GREEN_700),
                            ft.Text(
                                "Todos los productos del pedido están correctamente registrados en el mapeo.",
                                color=Colors.GREEN_900,
                            ),
                        ]
                    ),
                )
            )
            return

        count = len(no_mapeados)
        self.alerts_badge.bgcolor = Colors.ORANGE_100
        self.alerts_badge.content = ft.Text(
            f"{count} no mapeado(s)",
            size=12,
            weight=ft.FontWeight.W_600,
            color=Colors.ORANGE_900,
        )

        self.alerts_list.controls.append(
            ft.Container(
                padding=10,
                border_radius=8,
                bgcolor=Colors.ORANGE_50,
                border=ft.border.all(1, Colors.ORANGE_300),
                content=ft.Text(
                    "⚠️ ¡ATENCIÓN! Estos productos no están registrados en el mapeo y se omitieron en la plantilla:",
                    weight=ft.FontWeight.W_600,
                    color=Colors.ORANGE_900,
                ),
            )
        )

        for idx, prod in enumerate(no_mapeados, start=1):
            self.alerts_list.controls.append(
                ft.Container(
                    padding=ft.padding.symmetric(horizontal=12, vertical=8),
                    border_radius=6,
                    bgcolor=Colors.WHITE,
                    border=ft.border.all(1, Colors.ORANGE_200),
                    content=ft.Row(
                        controls=[
                            ft.Icon(Icons.ERROR_OUTLINE, color=Colors.RED_600, size=18),
                            ft.Text(f"{idx}. {prod}", selectable=True, expand=True),
                        ]
                    ),
                )
            )
