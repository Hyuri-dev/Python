import flet as ft

class myApp(ft.Column):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.vista_productos = ft.Column()
        self.width = 600

        # Crear el diálogo modal una sola vez
        self.dialog_form = ft.AlertDialog(
            modal=True,
            title=ft.Text("Nuevo Producto"),
            content=ft.Column([
                ft.TextField(label="Producto", width=300),
                ft.TextField(label="Precio", width=300),
                ft.Dropdown(
                    label="Condición",
                    options=[
                        ft.dropdown.Option("Nuevo"),
                        ft.dropdown.Option("Usado"),
                        ft.dropdown.Option("Reacondicionado")
                    ],
                    width=300
                ),
                ft.TextField(label="Ubicación", width=300),
            ], tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=self.cerrar_dialogo),
                ft.FilledButton("Guardar", on_click=self.guardar_producto)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        # Widgets
        self.text_bar = ft.TextField(hint_text="Escriba un producto ")
        self.button_create = ft.FilledButton(
            text="Crear Producto",
            on_click=self.abrir_formulario,
            icon=ft.Icons.ADD_OUTLINED,
            bgcolor='#02B431'
        )
        self.controls = [
            ft.Row(controls=[self.text_bar, self.button_create]),
            self.vista_productos
        ]

    def abrir_formulario(self, e):
        self.page.dialog = self.dialog_form
        self.dialog_form.open = True
        self.page.update()

    def cerrar_dialogo(self, e):
        self.dialog_form.open = False
        self.page.update()

    def guardar_producto(self, e):
        # Aquí procesarías los datos del formulario
        self.cerrar_dialogo(e)
        # Agregar producto a la vista
        self.vista_productos.controls.append(
            ft.Text("Producto agregado correctamente")
        )
        self.update()

def main(page: ft.Page):
    page.title = "Manejador de precios 2"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    # El diálogo debe ser una propiedad de la página, por lo tanto
    # lo asignamos al principio.
    app = myApp(page)
    page.add(app)
    page.update()

ft.app(target=main)