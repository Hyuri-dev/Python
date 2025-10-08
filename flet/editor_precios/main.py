import flet as ft

class myApp(ft.Column):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.vista_productos = ft.Column()
        self.width = 600
        
        # Widgets
        self.text_bar = ft.TextField(hint_text="Escriba un producto ")
        self.button_create = ft.FilledButton(
            text="Crear Producto", 
            on_click=self.crear_producto, 
            icon=ft.Icons.ADD_OUTLINED, 
            bgcolor='#02B431'
        )
        self.controls = [
            ft.Row(controls=[self.text_bar, self.button_create]),
            self.vista_productos
        ]
    
    # Método correctamente indentado (fuera del __init__)
    def crear_producto(self, e):
        # Aquí usas los valores de los campos para crear el producto
        producto = self.text_bar.value  # Ejemplo: obtener el texto del campo
        # Lógica para agregar el producto a la vista
        self.vista_productos.controls.append(
            ft.Text(f"Producto: {producto}")
        )
        self.update()  # Actualiza la interfaz

def main(page: ft.Page):
    page.title = "Manejador de precios"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    app = myApp(page)  # Solo pasamos 'page' como argumento
    page.add(app)
    page.update()

ft.app(target=main)