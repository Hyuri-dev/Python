import flet as ft


class myApp(ft.Column):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.monto = ft.TextField(label="Monto" ,width= 300, border_color="blue" )
        self.montoDeRetencion = ft.TextField(hint_text=f"Monto a Pagar Bs " ,width= 300 , read_only=True, border_color="GREEN", color="blue")
        self.montoARetener = ft.TextField(hint_text=f"Monto a Retener Bs " ,width= 300 , read_only=True, border_color="ORANGE", color="blue")


        # Widgets de la app 
        # El controls nos permite ingresar columnas y filas para renderizar nuestros widgets

        self.controls = [ft.Column(
            controls=[ft.Container(content=(ft.Column(controls= 
                                                      [ft.Row(controls=[ft.Text(value=f"Calculadora de retenciones ", size= 30, text_align="CENTER", width= 200 ), ft.Icon(name=ft.Icons.CALCULATE, size= 60)]),
                                                      self.monto, self.montoDeRetencion, self.montoARetener ,ft.Button(text="Calcular", width=300, on_click= self.CalcularRetencion), ft.Button(text="Limpiar",icon=ft.Icons.CLEAR, width=300, on_click=self.limpiarCampos)])), width= 350 , padding= 30 ) ]
        )]


        # Metodos / funciones de la app

    def CalcularRetencion(self,e):
      
      #Obtenemos el monto del input y se formatea
      self.input_monto = self.monto.value
      self.formateo = self.input_monto.replace(",", ".")
      self.input_monto = self.formateo
      
      #Constante IVA
      self.IVA = 0.75
      
      #Calculo de la retencion del 75% que retiene el negocio y el 25% que debe pagar el cliente
      self.monto_retencion = float(self.input_monto) * self.IVA
      self.montoAPagar = float(self.input_monto) * 0.25
      self.montoDeRetencion.value = f"Monto A Cancelar Bs.{self.montoAPagar}"
      self.montoARetener.value = f"Monto A Retener Bs.{self.monto_retencion}"
      
      
      self.page.update()
    
    def limpiarCampos(self, e):
      self.monto.value =""
      self.montoDeRetencion.value = f"Monto a Cancelar Bs."
      self.montoARetener.value = f"Monto a Retener Bs."
      
      self.page.update()
      



def main(page: ft.Page):
    page.title = "Calculadora de Retenciones"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    app = myApp(page)
    page.add(app)
    page.bgcolor="#141414"
    page.update()

ft.app(target=main)