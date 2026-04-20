import flet as ft

def main(page: ft.Page):
    # Configuración básica de la ventana/pantalla
    page.title = "Punto de Venta"
    page.theme_mode = ft.ThemeMode.LIGHT # O DARK, según prefieras
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Un componente de prueba
    mensaje = ft.Text(
        value="¡Flet está instalado y funcionando!",
        size=24,
        weight=ft.FontWeight.BOLD
    )

    # Agregamos el componente a la pantalla
    page.add(mensaje)

if __name__ == "__main__":
    # Iniciamos la app de Flet
    ft.app(target=main)
