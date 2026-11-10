from typing import Callable, Optional
import flet as ft

from config.settings import SettingsManager
from ui.components.file_selector import Colors, FileSelector, Icons, show_snackbar


class SettingsView(ft.Container):
    """
    Vista dedicada de Configuración (y Onboarding en primera ejecución):
    Permite visualizar, explorar con ft.FilePicker, validar existencia
    y guardar las rutas persistentes en config.json.
    """

    def __init__(
        self,
        page: ft.Page,
        settings_manager: SettingsManager,
        on_saved: Optional[Callable[[], None]] = None,
        is_onboarding: bool = False,
    ) -> None:
        super().__init__(expand=True, padding=24)
        self.host_page = page
        self.settings_manager = settings_manager
        self.on_saved = on_saved
        self.is_onboarding = is_onboarding

        current_config = self.settings_manager.load()

        self.pedidos_field = FileSelector(
            page=self.host_page,
            label="1. Ruta por defecto de Pedidos (Archivo o Carpeta)",
            value=current_config.get("ruta_pedidos_defecto", ""),
            hint_text="Ej: C:\\...\\pedidos.xlsx o carpeta de pedidos",
            helper_text="Archivo puntual o carpeta donde se ubican los pedidos diarios.",
            mode="both",
        )

        self.productos_field = FileSelector(
            page=self.host_page,
            label="2. Archivo de Mapeo de Productos (productos.xlsx)",
            value=current_config.get("ruta_productos", ""),
            hint_text="Ej: C:\\...\\productos.xlsx",
            helper_text="Catálogo Excel con columnas 'PRODUCTOS-SISTEMA' y 'COLUMNA-PLANTILLA'.",
            mode="file",
        )

        self.salida_field = FileSelector(
            page=self.host_page,
            label="3. Ruta de Salida del Consolidado (Carpeta o Archivo .xlsx)",
            value=current_config.get("ruta_salida", ""),
            hint_text="Ej: C:\\...\\salida o archivo plantilla_con_pedidos_cargados.xlsx",
            helper_text="Carpeta destino o ruta completa del archivo Excel consolidado final.",
            mode="both",
        )

        self.plantilla_field = FileSelector(
            page=self.host_page,
            label="4. Archivo de Plantilla Base (plantilla_pedidos.xlsx)",
            value=current_config.get("ruta_plantilla", ""),
            hint_text="Ej: C:\\...\\plantilla_pedidos.xlsx",
            helper_text="Plantilla de OpenPyXL con encabezados y fórmulas predefinidas.",
            mode="file",
        )

        self.validation_box = ft.Container(
            visible=False,
            padding=12,
            border_radius=8,
            bgcolor=Colors.RED_50,
            border=ft.border.all(1, Colors.RED_400),
            content=ft.Column(spacing=4, controls=[]),
        )

        self.save_button = ft.ElevatedButton(
            text="Guardar Configuración y Continuar" if is_onboarding else "Guardar Cambios",
            icon=Icons.SAVE_ROUNDED,
            style=ft.ButtonStyle(
                bgcolor=Colors.BLUE_700,
                color=Colors.WHITE,
                padding=ft.padding.symmetric(horizontal=24, vertical=16),
            ),
            on_click=self._handle_save,
        )

        onboarding_banner = ft.Container(
            visible=self.is_onboarding,
            padding=14,
            border_radius=10,
            bgcolor=Colors.AMBER_50,
            border=ft.border.all(1, Colors.AMBER_400),
            content=ft.Row(
                controls=[
                    ft.Icon(Icons.INFO_OUTLINE, color=Colors.AMBER_900),
                    ft.Text(
                        "¡Bienvenido! Es la primera ejecución o faltan rutas clave en 'config.json'. "
                        "Por favor selecciona las ubicaciones obligatorias para comenzar.",
                        expand=True,
                        weight=ft.FontWeight.W_500,
                        color=Colors.AMBER_900,
                    ),
                ]
            ),
        )

        self.content = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            spacing=18,
            controls=[
                ft.Column(
                    spacing=2,
                    controls=[
                        ft.Text(
                            "Configuración Inicial Obligatoria"
                            if self.is_onboarding
                            else "Configuración de Rutas",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            "Define las rutas persistentes almacenadas en config.json.",
                            size=14,
                            color=Colors.GREY_700,
                        ),
                    ],
                ),
                onboarding_banner,
                ft.Divider(height=1),
                ft.Container(
                    padding=20,
                    border_radius=12,
                    border=ft.border.all(1, Colors.GREY_300),
                    content=ft.Column(
                        spacing=18,
                        controls=[
                            self.pedidos_field,
                            self.productos_field,
                            self.salida_field,
                            self.plantilla_field,
                            self.validation_box,
                            ft.Row(
                                alignment=ft.MainAxisAlignment.END,
                                controls=[self.save_button],
                            ),
                        ],
                    ),
                ),
            ],
        )

    def reload_fields(self) -> None:
        config = self.settings_manager.load()
        self.pedidos_field.value = config.get("ruta_pedidos_defecto", "")
        self.productos_field.value = config.get("ruta_productos", "")
        self.salida_field.value = config.get("ruta_salida", "")
        self.plantilla_field.value = config.get("ruta_plantilla", "")
        self.validation_box.visible = False
        self.host_page.update()

    def _handle_save(self, _: ft.ControlEvent) -> None:
        candidate_config = {
            "ruta_pedidos_defecto": self.pedidos_field.value,
            "ruta_productos": self.productos_field.value,
            "ruta_salida": self.salida_field.value,
            "ruta_plantilla": self.plantilla_field.value,
        }

        is_valid, errors = self.settings_manager.validate_paths(
            candidate_config,
            require_template=bool(candidate_config["ruta_plantilla"]),
        )

        if not is_valid:
            error_controls = [
                ft.Row(
                    controls=[
                        ft.Icon(Icons.ERROR_OUTLINE, color=Colors.RED_700, size=18),
                        ft.Text(err, color=Colors.RED_900, size=13),
                    ]
                )
                for err in errors
            ]
            self.validation_box.content = ft.Column(spacing=4, controls=error_controls)
            self.validation_box.visible = True
            show_snackbar(
                self.host_page,
                "⚠️ Por favor corrige las rutas inválidas antes de guardar.",
                bgcolor=Colors.RED_700,
            )
            self.host_page.update()
            return

        self.validation_box.visible = False
        self.settings_manager.save(candidate_config)
        show_snackbar(
            self.host_page,
            "✅ Configuración guardada correctamente en 'config.json'.",
            bgcolor=Colors.GREEN_700,
        )

        if self.on_saved:
            self.on_saved()
        self.host_page.update()
