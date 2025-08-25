import flet as ft

class Contador :
    def __init__(self,page):
            self.counter = 0
            self.txt_counter = ft.Text(f"{self.counter}", size = 20)
            self.mensaje = ft.Text("", color = "red")
            self.btn = ft.ElevatedButton("incrementar", on_click = self.on_click)
            page.add(self.txt_counter,self.btn, self.mensaje)
    
    def on_click(self,e):
        self.counter +=1
        self.txt_counter.value =f"{self.counter}"
        if self.counter > 5:
            self.mensaje.value = "Gracias por probar la app, te amo ❤️"
        e.page.update()

def main(page):
    Contador(page)

ft.app(main)
