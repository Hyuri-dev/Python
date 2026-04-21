import flet as ft
from src.modules.sales import get_resumen
from src.modules.products import get_products

def main(page: ft.Page):
    BG_COLOR = "#284A3B"       # Verde oscuro de fondo
    CARD_COLOR = "#3C7961"     # Verde medio para tarjetas y barra inferior
    ACCENT_COLOR = "#1DAB77"   # Verde brillante para el botón +
    ICON_BG = "#214434"        # Verde muy oscuro para el fondo de los íconos

    page.bgcolor = BG_COLOR
    page.padding = 20
    page.theme_mode = ft.ThemeMode.DARK

    #--- Obtener datos de la BD ---

    productos_db= get_products()

    datos_hoy = get_resumen()
    total_ventas = str(datos_hoy.get("cantidad_ventas", 0))
    total_dinero = f"{datos_hoy.get('total_dinero', 0):.2f} Bs."



    header = ft.Row( controls=[
        ft.Text("Resumen del dia", size= 28, weight="bold"),
        ft.IconButton(
            icon = ft.icons.Icons.SHOPPING_CART_OUTLINED,
            bgcolor=CARD_COLOR,
            icon_color = ft.Colors.WHITE,
            icon_size=20,
            on_click= lambda e: print("Ver Carrito")
        )
    ], alignment= ft.MainAxisAlignment.SPACE_BETWEEN)
    
    def crear_tarjeta (icono, titulo,valor):
        return ft.Container(
            content= ft.Column([
                ft.Container(
                    content= ft.Icon(icono, color=ft.Colors.WHITE, size= 18),
                    bgcolor=ICON_BG,
                    width= 36, height=36,
                    border_radius= 21,
                    alignment=ft.Alignment.CENTER
                ),
                ft.Container(height=5),
                ft.Text(titulo, size = 16),
                ft.Text(valor, size= 32, weight="bold")
            ]),
            bgcolor=CARD_COLOR,
            border_radius= 15,
            padding= 15,
            expand= True
        )
    
    fila_resumen = ft.Row(
        controls=[
            crear_tarjeta(ft.Icons.SELL_OUTLINED, "Ventas", total_ventas),
            crear_tarjeta(ft.Icons.ATTACH_MONEY, "Dinero", total_dinero)

        ], spacing= 15
    )
    # ---- Lista de productos ----
    lista_productos =  ft.ListView(
        expand=True,
        spacing=15,
        padding=ft.padding.Padding.only(bottom=80)
    )

    def crear_tarjeta_producto(producto):
        return ft.Container(
            content= ft.Row(
                controls=[
                    ft.Container(
                        content= ft.Icon(ft.Icons.LOCAL_DRINK, color= ft.Colors.WHITE, size=30), width= 70, height=70,
                        bgcolor=ICON_BG,
                        border_radius= 10,
                        alignment=ft.Alignment.CENTER
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(producto['nombre'], size=18, weight="bold"),
                            ft.Text(f"{producto['precio_base']:.2f} Bs.", size=16, color=ACCENT_COLOR, weight="w600")
                        ], expand= True, spacing= 5
                    ),
                    ft.IconButton(
                        icon=ft.Icons.ADD_CIRCLE,
                        icon_color=ACCENT_COLOR,
                        icon_size=35,
                        on_click= lambda e: print(f"Añadido: {producto['nombre']}")
                    )
                ], alignment= ft.MainAxisAlignment.SPACE_BETWEEN
            ), bgcolor= CARD_COLOR,
            border_radius=15,
            padding=15
        )
    
    if not productos_db:
        lista_productos.controls.append(
            ft.Text("No hay productos registrados aún", color= ft.Colors.WHITE_54,text_align="center")
        )
    else:
        for prod in productos_db:
            lista_productos.controls.append(crear_tarjeta_producto(prod))

    # --- Barra inferior ---

    page.floating_action_button = ft.FloatingActionButton(
        icon = ft.Icons.ADD,
        bgcolor=ACCENT_COLOR,
        shape=ft.CircleBorder(),
        on_click= lambda e: print("Acción principal")
    )
    page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED

    page.bottom_appbar = ft.BottomAppBar(
        bgcolor=CARD_COLOR,
        content= ft.Row(
            controls=[
                ft.Container(content= ft.Text("Ventas", weight="bold", text_align="center", size=24), expand=True),
                ft.Container(width=60), #Espacio para el boton del medio
                ft.Container(content = ft.Text("Productos", weight = "bold", text_align="center", size=24), expand= True)

            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
    )

    page.add(
        header,
        ft.Container(height=10),
        fila_resumen,
        ft.Container(height= 20),
        ft.Text("Productos", size= 20, weight="bold"),
        lista_productos
    )

if __name__ == "__main__":
    ft.app(target=main)