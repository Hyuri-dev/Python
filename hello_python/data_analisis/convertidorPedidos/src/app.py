"""UI minimalista (Flet) para el convertidor de pedidos.

Ejecutar desde la raíz del proyecto:
    python src/app.py
"""
import asyncio
import os
from pathlib import Path

import flet as ft

from convertidor import ConversionError, procesar_pedidos


def main(page: ft.Page):
    page.title = "Convertidor de Pedidos"
    page.window.width = 520
    page.window.height = 440
    page.padding = 30
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    estado = {"ruta": None, "salida": None}

    # ---------- Controles ----------
    txt_archivo = ft.Text("Ningún archivo seleccionado", color=ft.Colors.GREY_600, size=13)
    barra = ft.ProgressBar(visible=False, width=440)  # indeterminada (value=None)
    txt_progreso = ft.Text("Procesando pedidos...", size=12, visible=False, color=ft.Colors.GREY_700)

    icono_msg = ft.Icon(ft.Icons.INFO_OUTLINE, size=20)
    txt_msg = ft.Text("", size=13, selectable=True, expand=True)
    caja_msg = ft.Container(
        content=ft.Row([icono_msg, txt_msg], vertical_alignment=ft.CrossAxisAlignment.START),
        padding=12,
        border_radius=8,
        width=440,
        visible=False,
    )

    def notificar(mensaje: str, tipo: str = "info"):
        """Muestra el mensaje en la caja de estado y en un SnackBar."""
        estilos = {
            "ok": (ft.Icons.CHECK_CIRCLE_OUTLINE, ft.Colors.GREEN_700, ft.Colors.GREEN_50),
            "warn": (ft.Icons.WARNING_AMBER, ft.Colors.ORANGE_800, ft.Colors.ORANGE_50),
            "error": (ft.Icons.ERROR_OUTLINE, ft.Colors.RED_700, ft.Colors.RED_50),
            "info": (ft.Icons.INFO_OUTLINE, ft.Colors.BLUE_700, ft.Colors.BLUE_50),
        }
        icon, color, fondo = estilos[tipo]
        icono_msg.icon, icono_msg.color = icon, color
        txt_msg.value, txt_msg.color = mensaje, color
        caja_msg.bgcolor = fondo
        caja_msg.visible = True

        snack = ft.SnackBar(ft.Text(mensaje.splitlines()[0]), bgcolor=color)
        page.show_dialog(snack)
        page.update()

    # ---------- Selección de archivo ----------
    def aplicar_seleccion(files):
        if not files:
            return
        estado["ruta"] = files[0].path
        txt_archivo.value = Path(estado["ruta"]).name
        txt_archivo.color = ft.Colors.BLACK
        btn_procesar.disabled = False
        btn_abrir.visible = False
        caja_msg.visible = False
        page.update()

    file_picker = ft.FilePicker()
    page.services.append(file_picker)

    async def seleccionar(_):
        aplicar_seleccion(
            await file_picker.pick_files(
                dialog_title="Selecciona el archivo de pedidos",
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=["xlsx", "xls"],
                allow_multiple=False,
            )
        )

    # ---------- Procesamiento ----------
    def set_cargando(cargando: bool):
        barra.visible = txt_progreso.visible = cargando
        btn_procesar.disabled = btn_cargar.disabled = cargando
        if cargando:
            caja_msg.visible = False
            btn_abrir.visible = False
        page.update()

    async def procesar(_):
        if not estado["ruta"]:
            notificar("Primero selecciona un archivo de Excel.", "warn")
            return

        set_cargando(True)
        try:
            # Se ejecuta en un hilo aparte para no congelar la UI
            res = await asyncio.to_thread(procesar_pedidos, estado["ruta"])
        except ConversionError as ex:
            set_cargando(False)
            notificar(str(ex), "error")
            return
        except Exception as ex:  # errores inesperados
            set_cargando(False)
            notificar(f"Error inesperado: {type(ex).__name__}: {ex}", "error")
            return

        set_cargando(False)
        estado["salida"] = res["salida"]
        btn_abrir.visible = True
        msg = f"Filtrado exitoso: {res['clientes']} clientes procesados.\nGuardado en: {res['salida']}"
        if res["no_mapeados"]:
            msg += "\n\nProductos sin mapeo (omitidos):\n• " + "\n• ".join(res["no_mapeados"])
            notificar(msg, "warn")
        else:
            notificar(msg, "ok")

    def abrir_salida(_):
        if estado["salida"] and os.path.exists(estado["salida"]):
            os.startfile(estado["salida"])  # Windows

    # ---------- Botones ----------
    btn_cargar = ft.OutlinedButton("Cargar Excel", icon=ft.Icons.UPLOAD_FILE, on_click=seleccionar)
    btn_procesar = ft.FilledButton("Procesar", icon=ft.Icons.PLAY_ARROW, on_click=procesar, disabled=True)
    btn_abrir = ft.TextButton("Abrir resultado", icon=ft.Icons.OPEN_IN_NEW, on_click=abrir_salida, visible=False)

    # ---------- Layout ----------
    page.add(
        ft.Column(
            [
                ft.Text("Convertidor de Pedidos", size=22, weight=ft.FontWeight.BOLD),
                ft.Text("Carga el Excel de pedidos y conviértelo a la plantilla.",
                        size=13, color=ft.Colors.GREY_600),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                ft.Row([btn_cargar, txt_archivo], spacing=12),
                ft.Row([btn_procesar, btn_abrir], spacing=12),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                barra,
                txt_progreso,
                caja_msg,
            ],
            spacing=12,
            width=440,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
    )


if __name__ == "__main__":
    ft.run(main)
