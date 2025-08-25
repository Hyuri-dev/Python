import flet as ft

class MyApp(ft.Column) :
    def __init__(self,page):
            self.counter = 0
            
            self.txt_counter = ft.Text(f"{self.counter}", size = 20)
            self.mensaje = ft.Text("", color = "red")
            
            
            self.btn = ft.FloatingActionButton(icon = ft.Icons.ADD, on_click = self.on_click)
            # page.add(self.txt_counter,self.btn, self.mensaje)
            
            
            page.add(
                ft.Column(
                  controls = [
                    ft.Row(
                      controls = [
                        self.txt_counter,
                        self.btn
                      ],
                      alignment = ft.MainAxisAlignment.CENTER #Alineación horizontal
                    ),
                    self.mensaje
                  ], horizontal_alignment = ft.CrossAxisAlignment.CENTER #Centra columna completa
                  
                )
            )
    
    def on_click(self,e):
        self.counter +=1
        self.txt_counter.value =f"{self.counter}"
        if self.counter > 5:
            self.mensaje.value = "Gracias por probar la app, te amo ❤️"
        self.txt_counter.update
        e.page.update()

def main(page):
    page.title = "Contador de Flet"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    MyApp(page)
    

ft.app(target = main)
