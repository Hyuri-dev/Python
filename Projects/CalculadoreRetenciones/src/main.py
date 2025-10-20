import flet as ft


class myApp(ft.Column):
    def __init__(self, page):
        super().__init__()
        self.page = page

        # Widgets de la app 
        self.text = ft.Text(value="Hola, Este es mi hola mundo :)!")

        self.controls = [ft.Column(
            controls=[ft.Container(content=(ft.Column(controls= 
                                                      [ft.Text(value="Calculadora de retenciones", size= 30, text_align="CENTER", width= 300),
                                                       ft.TextField(label="Monto", width= 300), ft.TextField(hint_text="Resultado", value=f"Monto a pagar: ", disabled=True, width= 300), ft.Button(text="Calcular", width=300)])), width= 350 , padding= 30 ) ]
        )]


def main(page: ft.Page):
    page.title = "Calculadora de Retenciones"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    app = myApp(page)  # Solo pasamos 'page' como argumento
    page.add(app)
    page.bgcolor="#141414"
    page.update()

ft.app(target=main)