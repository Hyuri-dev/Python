import asyncio
import flet as ft
from convertidor import procesar_pedidos


async def main(page: ft.Page):
    page.align_items = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    archivo_seleccionado = {"path": None}

    CLAVE_MAPEO = "convertidor_app.rutas"
    CLAVE_SALIDA = "convertidor_app.ruta_salida"
    CLAVE_MODELO = "convertidor_app.ruta_modelo"
    prefs = ft.SharedPreferences()

    ruta_mapeo_inicial = await prefs.get(CLAVE_MAPEO)
    ruta_salida_inicial = await prefs.get(CLAVE_SALIDA)
    ruta_modelo_inicial = await prefs.get(CLAVE_MODELO)

    txt_ruta = ft.Text(
        value=f"Ruta de mapeo de productos: {ruta_mapeo_inicial or 'No configurada'}",
        selectable=True,
        color=ft.Colors.BLUE_700,
    )
    txt_ruta_salida = ft.Text(
        value=f"Ruta de salida de archivos: {ruta_salida_inicial or 'No configurada'}",
        selectable=True,
        color=ft.Colors.BLUE_700,
    )
    txt_ruta_modelo = ft.Text(
        value=f"Ruta del modelo: {ruta_modelo_inicial or 'No configurada'}",
        selectable=True,
        color=ft.Colors.BLUE_700,
    )

    warning_text = ft.Text(value="Ningún Archivo Seleccionado", size=20)

    async def on_files_selected(e: ft.FilePickerResultEvent):
        if e.files:
            archivo_seleccionado["path"] = e.files[0].path
            warning_text.value = f"Archivo seleccionado: {archivo_seleccionado['path']}"
            boton_convertir.disabled = False
        else:
            warning_text.value = "Selección cancelada"
            archivo_seleccionado["path"] = None
            boton_convertir.disabled = True
        page.update()

    async def on_mapeo_selected(e: ft.ControlEvent):
        archivo = await ft.FilePicker().pick_files(
            allow_multiple=False,
            dialog_title="Seleccione el archivo de mapeo",
            allowed_extensions=["xlsx", "xls"],
        )
        if archivo:
            ruta = archivo[0].path
            await prefs.set(CLAVE_MAPEO, ruta)
            txt_ruta.value = f"Ruta de mapeo de productos: {ruta}"
            page.update()

    async def on_ruta_salida_selected(e: ft.ControlEvent):
        carpeta = await ft.FilePicker().get_directory_path(
            dialog_title="Seleccione la carpeta para guardar el archivo"
        )
        if carpeta:
            await prefs.set(CLAVE_SALIDA, carpeta)
            txt_ruta_salida.value = f"Ruta de salida de archivos: {carpeta}"
            page.update()

    async def on_ruta_modelo_selected(e: ft.ControlEvent):
        archivo = await ft.FilePicker().pick_files(
            allow_multiple=False,
            dialog_title="Seleccione el archivo del modelo",
            allowed_extensions=["xlsx", "xls"],
        )
        if archivo:
            ruta = archivo[0].path
            await prefs.set(CLAVE_MODELO, ruta)
            txt_ruta_modelo.value = f"Ruta del modelo: {ruta}"
            page.update()

    async def convertir_archivo(e):
        # 1. Leer siempre los valores actualizados desde SharedPreferences
        ruta_pedidos = archivo_seleccionado["path"]
        ruta_mapeo = await prefs.get(CLAVE_MAPEO)
        ruta_salida = await prefs.get(CLAVE_SALIDA)
        ruta_modelo = await prefs.get(CLAVE_MODELO)

        # 2. Validar que las 4 rutas existan antes de llamar a procesar_pedidos
        if not all([ruta_pedidos, ruta_mapeo, ruta_salida, ruta_modelo]):
            warning_text.value = "⚠️ Faltan rutas por configurar en el menú superior."
            page.update()
            return

        warning_text.value = "Procesando el archivo, espere..."
        boton_convertir.disabled = True
        page.update()

        try:
            # 3. Ejecutar en hilo separado sin bloquear la UI
            salida = await asyncio.to_thread(
                procesar_pedidos,
                ruta_pedidos,
                ruta_mapeo,
                ruta_salida,
                ruta_modelo,
            )
            warning_text.value = f"✅ Archivo guardado como: {salida}"
        except Exception as ex:
            warning_text.value = f"❌ Error durante la conversión: {ex}"
        finally:
            boton_convertir.disabled = False
            page.update()

    page.appbar = ft.AppBar(
        bgcolor=ft.Colors.GREY_900,
        leading=ft.Icon(ft.Icons.MENU),
        leading_width=20,
        title=ft.Text(
            "Convertidor de Pedidos",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
        ),
        elevation=0,
        actions=[
            ft.PopupMenuButton(
                key="popup",
                items=[
                    ft.PopupMenuItem(
                        content="Configurar ruta de plantilla",
                        on_click=on_mapeo_selected,
                    ),
                    ft.PopupMenuItem(
                        content="Configurar ruta de salida",
                        on_click=on_ruta_salida_selected,
                    ),
                    ft.PopupMenuItem(
                        content="Configurar ruta del modelo",
                        on_click=on_ruta_modelo_selected,
                    ),
                ],
            )
        ],
    )

    title = ft.Text(
        value="Ingrese el archivo de pedidos a convertir",
        size=30,
        weight=ft.FontWeight.BOLD,
    )

    file_picker = ft.FilePicker(on_result=on_files_selected)
    page.services.append(file_picker)

    boton_abrir = ft.Button(
        "Buscar Archivo",
        icon=ft.Icons.UPLOAD_FILE,
        action=ft.PickFiles(
            file_picker,
            allow_multiple=False,
            dialog_title="Seleccione un archivo",
            allowed_extensions=["xlsx", "xls"],
        ),
    )

    boton_convertir = ft.Button(
        "Convertir Archivo",
        icon=ft.Icons.PLAY_ARROW,
        disabled=True,
        on_click=convertir_archivo,
    )

    page.add(
        title,
        warning_text,
        boton_abrir,
        ft.Divider(height=20, color=ft.Colors.BLUE_50),
        boton_convertir,
        txt_ruta,
        txt_ruta_salida,
        txt_ruta_modelo,
    )


ft.run(main)
# class GestorPedidosApp:
#     """Controlador principal de la aplicación de escritorio en Flet."""

#     def __init__(self, page: ft.Page):
#         self.page = page
#         self.settings_manager = SettingsManager()

#         self._configure_window()

#         self.converter_view = ConverterView(
#             page=self.page,
#             settings_manager=self.settings_manager,
#             on_open_settings=lambda: self.navigate_to(1),
#         )
#         self.settings_view = SettingsView(
#             page=self.page,
#             settings_manager=self.settings_manager,
#             on_saved=self._on_settings_saved,
#             is_onboarding=not self.settings_manager.is_configured(),
#         )

#         self.nav_rail = ft.NavigationRail(
#             selected_index=0,
#             label_type=ft.NavigationRailLabelType.ALL,
#             min_width=100,
#             min_extended_width=200,
#             group_alignment=-0.9,
#             destinations=[
#                 ft.NavigationRailDestination(
#                     icon=Icons.SYNC_ALT_OUTLINED,
#                     selected_icon=Icons.SYNC_ALT,
#                     label="Conversor",
#                 ),
#                 ft.NavigationRailDestination(
#                     icon=Icons.SETTINGS_OUTLINED,
#                     selected_icon=Icons.SETTINGS,
#                     label="Configuración",
#                 ),
#             ],
#             on_change=self._on_nav_change,
#         )

#         self.body_container = ft.Container(expand=True)

#         self.page.add(
#             ft.Row(
#                 expand=True,
#                 spacing=0,
#                 controls=[
#                     self.nav_rail,
#                     ft.VerticalDivider(width=1),
#                     self.body_container,
#                 ],
#             )
#         )

#         self._check_initial_onboarding()

#     def _configure_window(self) -> None:
#         self.page.title = "Gestor y Convertidor de Pedidos"
#         self.page.theme_mode = ft.ThemeMode.LIGHT
#         self.page.padding = 0
#         if hasattr(self.page, "window"):
#             self.page.window.width = 980
#             self.page.window.height = 720
#             self.page.window.min_width = 800
#             self.page.window.min_height = 600
#         else:
#             self.page.window_width = 980
#             self.page.window_height = 720
#             self.page.window_min_width = 800
#             self.page.window_min_height = 600

#     def _check_initial_onboarding(self) -> None:
#         """
#         Onboarding (Primera ejecución):
#         Si config.json no existe o las rutas clave están vacías, redirige a la pantalla
#         de configuración obligatoria y muestra un diálogo modal informativo.
#         """
#         if not self.settings_manager.is_configured():
#             self.nav_rail.selected_index = 1
#             self.nav_rail.disabled = True
#             self.body_container.content = self.settings_view
#             self.page.update()
#             self._show_onboarding_dialog()
#         else:
#             self.navigate_to(0)

#     def _show_onboarding_dialog(self) -> None:
#         def close_dialog(_: ft.ControlEvent) -> None:
#             dialog.open = False
#             if hasattr(self.page, "close"):
#                 try:
#                     self.page.close(dialog)
#                     return
#                 except Exception:
#                     pass
#             self.page.update()

#         dialog = ft.AlertDialog(
#             modal=True,
#             title=ft.Row(
#                 controls=[
#                     ft.Icon(Icons.SETTINGS_SUGGEST, color=Colors.BLUE_700),
#                     ft.Text("Configuración Inicial Requerida"),
#                 ]
#             ),
#             content=ft.Text(
#                 "No se detectó un archivo 'config.json' válido o algunas rutas clave están vacías.\n\n"
#                 "Por favor selecciona las ubicaciones de:\n"
#                 "• Ruta por defecto de pedidos\n"
#                 "• Archivo de mapeo de productos (productos.xlsx)\n"
#                 "• Ruta de salida para el consolidado final\n\n"
#                 "Una vez guardadas, podrás utilizar el conversor normalmente."
#             ),
#             actions=[
#                 ft.ElevatedButton(
#                     text="Configurar Ahora",
#                     bgcolor=Colors.BLUE_700,
#                     color=Colors.WHITE,
#                     on_click=close_dialog,
#                 )
#             ],
#             actions_alignment=ft.MainAxisAlignment.END,
#         )

#         if hasattr(self.page, "open"):
#             try:
#                 self.page.open(dialog)
#                 return
#             except Exception:
#                 pass
#         self.page.dialog = dialog
#         dialog.open = True
#         self.page.update()

#     def _on_settings_saved(self) -> None:
#         """Se ejecuta tras guardar exitosamente las rutas en config.json."""
#         self.nav_rail.disabled = False
#         self.settings_view.is_onboarding = False
#         self.converter_view.refresh_from_settings()
#         self.navigate_to(0)

#     def _on_nav_change(self, e: ft.ControlEvent) -> None:
#         index = e.control.selected_index
#         self.navigate_to(index)

#     def navigate_to(self, index: int) -> None:
#         if index == 0 and not self.settings_manager.is_configured():
#             self.nav_rail.selected_index = 1
#             self.body_container.content = self.settings_view
#             self.page.update()
#             return

#         self.nav_rail.selected_index = index
#         if index == 0:
#             self.converter_view.refresh_from_settings()
#             self.body_container.content = self.converter_view
#         else:
#             self.settings_view.reload_fields()
#             self.body_container.content = self.settings_view
#         self.page.update()


# def main(page: ft.Page) -> None:
#     GestorPedidosApp(page)


# if __name__ == "__main__":
#     ft.run(main)
