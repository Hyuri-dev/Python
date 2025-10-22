import flet as ft

class Info (ft.Column):
   def __init__(self, title , descripcion, valueTextField , color):
      super().__init__()
      self.spacing = 50
      self.titleWidget = ft.Text(value= title , weight= ft.FontWeight.BOLD, size= 16 ,color= color)
      self.descripcionWidget = ft.Text(value= descripcion, size = 14, color= color)
      self.inputWidget = ft.TextField(hint_text= valueTextField , width= 300 , read_only= True , border_color= color)

      self.controls =[ ft.Column(
         controls=[
            ft.Container(
               content=(
                  ft.Column(
                     controls= [
                        self.titleWidget,
                        self.descripcionWidget,
                        self.inputWidget
                     ],
                  width= 300, spacing= 10)
               )
            )
         ]
      )

      ]



class myApp(ft.Column):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.width = 350
        self.spacing = 15
        
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        self.monto = ft.TextField(label="Monto del IVA (Bs.)" ,width= 300, border_color="blue", keyboard_type=ft.KeyboardType.NUMBER, hint_text="Ej: 245.23")
        self.montoDeRetencion = ft.TextField(hint_text=f"Monto a Pagar Bs " ,width= 300 , read_only=True, border_color="GREEN", keyboard_type=ft.KeyboardType.NUMBER, input_filter=ft.NumbersOnlyInputFilter())
        self.montoARetener = ft.TextField(hint_text=f"Monto a Retener Bs " ,width= 300 , read_only=True, border_color="ORANGE", keyboard_type=ft.KeyboardType.NUMBER, input_filter=ft.NumbersOnlyInputFilter())
        self.descripcion = ft.Text(value= "Aqui encontraras una explicacion de esta calculadora sencilla para sacar las retenciones de tus facturas.", width= 300, size= 14)

        # Widgets del tutorial:

        self.dialogHelp = ft.AlertDialog(
           open=True,
           title= "Tutorial",
           content= ft.Column([
              self.descripcion,
              Info("Monto" , "La casilla monto es para que ingrese el monto del iva en Bolivares para asi calcular la retencion.", "Monto", "Blue" ),
              Info("Monto a Pagar Bs" , "La casilla Monto a pagar es el monto en Bolivares que el cliente te debe cancelar anexado al total de la factura en Bolivares .", "Monto a Pagar Bs", "GREEN" ),
              Info("Monto a Retener" , "La casilla Monto a Retener te inidicará cuanto sera el comprobante que debe darte el cliente.", "Monto a Retener", "ORANGE" )
           ]))


        # Widgets de la app 
        # El controls nos permite ingresar columnas y filas para renderizar nuestros widgets

        self.controls = [ft.Column(
            controls=[ft.Container(content=(ft.Column(controls= 
                                                      [ft.Row(controls=[ft.Text(value=f"Calculadora de Retenciones", size= 25, text_align="center", width= 200 ), ft.Icon(name=ft.Icons.CALCULATE, size= 40)]),
                                                      self.monto, self.montoDeRetencion, self.montoARetener ,ft.Button(text="Calcular", width=300, on_click= self.CalcularRetencion), ft.Button(text="Limpiar",icon=ft.Icons.CLEAR, width=300, on_click=self.limpiarCampos), ft.Button(text="Ayuda",icon=ft.Icons.HELP ,width=300,on_click=lambda e: self.page.open(self.dialogHelp))])), width= 350 , padding= 30 ) ]
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
      self.monto_retencion_redondeado = round(self.monto_retencion, 2)
      self.montoAPagar = float(self.input_monto) * 0.25
      self.montoDeRetencion.value = f"Monto A Cancelar Bs.{self.montoAPagar}"
      self.montoARetener.value = f"Monto A Retener Bs.{self.monto_retencion_redondeado}"
      
      
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
    page.theme_mode = ft.ThemeMode.SYSTEM
    
    app = myApp(page)
    page.add(app)
    page.bgcolor="#141414"
    page.update()

ft.app(target=main)