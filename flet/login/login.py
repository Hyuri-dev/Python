import flet as ft

class Login (ft.Column):
  def __init__(self,page):
    self.usuario = ""
    self.contraseña = ""
    
    # widgets 
    self.notificacion = ft.Text("", color = "red")
    self.lbl_user = ft.Text("Login", size = 40)
    self.entry_user = ft.TextField(label = "Usuario", hint_text = "Ingrese su usuario")
    
    self.lbl_password = ft.Text("Contraseña", size = 40)
    self.entry_password = ft.TextField(label = "Contraseña", hint_text = "Ingrese su contraseña" ,password= True, can_reveal_password = True)
    
    self.button_login = ft.ElevatedButton("Iniciar Sesión", on_click = self.verificar_credenciales)
    
    page.add(
      ft.Column(
        controls = [
          ft.Row(
            controls = [
              self.lbl_user,
              # self.lbl_password
            ], alignment = ft.MainAxisAlignment.CENTER
          ),
          self.entry_user,
          self.entry_password,
          self.button_login,
          self.notificacion
        ], alignment = ft.CrossAxisAlignment.CENTER
      )
    )
  
  def verificar_credenciales(self,e):
    if self.entry_user.value == "aquiles" and self.entry_password.value == "admin":
      self.notificacion.value = "Has iniciado sesión correctamente, Bienvenido!"
      self.notificacion.color = "green"
    else:
      self.notificacion.value = "Credenciales incorrectas"
      self.notificacion.color = "red"
    self.notificacion.update()
  
  

def main(page):
  page.title = "Login"
  page.vertical_alignment = ft.MainAxisAlignment.CENTER
  Login(page)

ft.app(target = main)