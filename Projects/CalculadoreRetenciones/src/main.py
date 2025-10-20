import flet as ft


class myApp(ft.Column):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.monto = ft.TextField(label="Monto" ,width= 300 )
        self.montoDeRetencion = ft.TextField(hint_text=f"Monto a Pagar " ,width= 300 , disabled=True)

        # Widgets de la app 
        self.text = ft.Text(value="Hola, Este es mi hola mundo :)!")

        self.controls = [ft.Column(
            controls=[ft.Container(content=(ft.Column(controls= 
                                                      [ft.Text(value="Calculadora de retenciones", size= 30, text_align="CENTER", width= 300),
                                                       self.monto, self.montoDeRetencion, ft.Button(text="Calcular", width=300, on_click= self.CalcularRetencion)])), width= 350 , padding= 30 ) ]
        )]


        # Metodos / funciones de la appp

    def CalcularRetencion(self,e):
      self.input_monto = self.monto.value
      self.IVA = 0.75
      self.monto_retencion = float(self.input_monto) * self.IVA
      self.montoAPagar = float(self.input_monto) * 0.25
      self.montoDeRetencion.value = f"Monto A Cancelar Bs.{self.montoAPagar}"
      self.page.update()


def main(page: ft.Page):
    page.title = "Calculadora de Retenciones"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    app = myApp(page)  # Solo pasamos 'page' como argumento
    page.add(app)
    page.bgcolor="#141414"
    page.update()

ft.app(target=main)