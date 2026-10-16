# main.py
import flet as ft
import script
from datetime import datetime


async def main(page: ft.Page):

    fecha_actual = datetime.now()
    fecha_formateada = fecha_actual.strftime("%d/%m/%Y")
    page.title = "Tasa BCV"
    page.window.width = 400
    # page.window_width = 200
    page.window_height = 520
    page.window_resizable = False
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#F3F4F6"

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # --- 1. Controles de la Tarjeta ---
    icono_encabezado = ft.Icon(
        ft.Icons.CURRENCY_EXCHANGE_ROUNDED,
        color=ft.Colors.BLUE_600,
        size=36,
    )

    titulo = ft.Text(
        f"Tasa Oficial BCV ",
        size=20,
        weight=ft.FontWeight.W_600,
        color=ft.Colors.BLUE_GREY_800,
    )

    subtitulo1 = ft.Text(
        "Dólar estadounidense (USD)",
        size=13,
        color=ft.Colors.BLUE_GREY_400,
    )

    subtitulo_date = ft.Text(
        f"Fecha: {fecha_formateada}",
        size= 12,
        color=ft.Colors.BLUE_ACCENT_200,
        weight=ft.FontWeight.W_400
    )

    barra_carga = ft.ProgressBar(
        width=260,
        color=ft.Colors.BLUE_600,
        bgcolor=ft.Colors.BLUE_50,
        border_radius=4,
        visible=False,
    )

    estado_txt = ft.Text(
        "Presiona actualizar para consultar",
        size=12,
        color=ft.Colors.GREY_600,
        italic=True,
    )

    resultado_txt = ft.Text(
        size=26,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.GREEN_700,
        visible=False,
    )

    tarjeta_principal = ft.Card(
        elevation=6,
        content=ft.Container(
            content=ft.Column(
                controls=[
                    icono_encabezado,
                    titulo,
                    subtitulo1,subtitulo_date,
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    resultado_txt,
                    barra_carga,
                    ft.Container(content=estado_txt, margin=ft.Margin.only(top=8)),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=4,
            ),
            width=320,
            padding=ft.Padding.symmetric(vertical=32, horizontal=24),
            bgcolor=ft.Colors.WHITE,
            border_radius=16,
        ),
    )

    # --- 2. Función para consultar / refrescar la tasa ---
    async def cargar_tasa(e=None):
        # Deshabilitar botón y activar estado de carga
        btn_actualizar.disabled = True
        barra_carga.visible = True
        resultado_txt.visible = False
        estado_txt.value = "Consultando tipo de cambio..."
        estado_txt.color = ft.Colors.GREY_600
        page.update()

        try:
            tasa = await script.obtener_bcv()
            resultado_txt.value = f"Bs. {tasa}"
            resultado_txt.color = ft.Colors.GREEN_700
            estado_txt.value = "Actualizado según banco central"
        except Exception as ex:
            resultado_txt.value = "Error"
            resultado_txt.color = ft.Colors.RED_600
            estado_txt.value = f"Fallo al consultar ({ex})"
        finally:
            barra_carga.visible = False
            resultado_txt.visible = True
            btn_actualizar.disabled = False
            page.update()

    # --- 3. Botón de Actualizar debajo de la tarjeta ---
    btn_actualizar = ft.FilledButton(
        content= ft.Row(
            controls=[ft.Icon("refresh", color=ft.Colors.WHITE),ft.Text("Actualizar tasa", ft.Colors.WHITE),],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8
        ),
        icon=ft.Icons.REFRESH_ROUNDED,
        on_click=cargar_tasa,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        height=45,
        width=50,
    )

    # --- 4. Ensamblar en la página ---
    page.add(
        tarjeta_principal,
        ft.Divider(height=16, color=ft.Colors.TRANSPARENT),
        btn_actualizar,
    )

    # Ejecutar una primera consulta automáticamente al abrir la app
    await cargar_tasa()


if __name__ == "__main__":
    ft.run(main)