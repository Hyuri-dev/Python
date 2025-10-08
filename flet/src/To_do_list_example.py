import flet as ft

class MyApp(ft.Column):
    def __init__(self, page):
        # Llama al constructor de la clase base
        super().__init__()
        
        self.page = page
        self.counter = 0
        
        # Define los controles de la UI
        self.txt_counter = ft.Text("0", size=20)
        self.mensaje = ft.Text("", color="red")
        
        self.btn = ft.FloatingActionButton(
            icon=ft.Icons.ADD,
            on_click=self.on_click
        )

        # Agrega los controles a la página en una fila centrada
        self.page.add(
            ft.Row(
                controls=[
                    self.txt_counter,
                    self.btn,
                    self.mensaje
                ],
                # Alineación horizontal para centrar los widgets
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
    
    def on_click(self, e):
        """Función que se ejecuta al hacer clic en el botón."""
        self.counter += 1
        
        # Actualiza el valor del contador
        self.txt_counter.value = f"{self.counter}"
        
        # Muestra el mensaje si el contador es mayor que 5
        if self.counter > 5:
            self.mensaje.value = "Gracias por probar la app, te amo ❤️"
        
        # Actualiza los widgets del contador y del mensaje para que los cambios se reflejen en la UI
        self.txt_counter.update()
        self.mensaje.update()

def main(page):
    """Función principal que inicializa la aplicación."""
    page.title = "Contador de Flet"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    MyApp(page)

ft.app(target=main)