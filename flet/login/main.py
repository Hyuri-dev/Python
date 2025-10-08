import flet as ft
import db
from models import Users

db.Base.metadata.create_all(db.engine)

class Login (ft.Column):
  def __init__(self,page):
    self.page = page
    self.modo_registro = False
    
    # widgets 
    self.notificacion = ft.Text("", color = "red")
    self.lbl_user = ft.Text("Login", size = 40)
    self.entry_user = ft.TextField(label = "Usuario", hint_text = "Ingrese su usuario")
    
    self.lbl_password = ft.Text("Contraseña", size = 40)
    self.entry_password = ft.TextField(label = "Contraseña", hint_text = "Ingrese su contraseña" ,password= True, can_reveal_password = True)
    
    self.button_login = ft.ElevatedButton("Iniciar Sesión", on_click = self.verificar_credenciales)
    self.button_register = ft.TextButton("Crear usuario", on_click = self.mostrar_registro)
    
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
          self.button_register,
          self.notificacion
        ], alignment = ft.CrossAxisAlignment.CENTER
      )
    )
  
  def mostrar_registro(self,e):
    self.modo_registro = True
    self.lbl_user.value = "Registro de usuario"
    self.lbl_user.color = "blue"
    self.button_login.text = "Registrar"
    self.button_login.on_click = self.crear_usuario
    self.notificacion.value = ""
    self.page.update()
  
  def verificar_credenciales(self,e):
    usuario = self.entry_user.value
    password = self.entry_password.value
    user = db.session.query(Users).filter_by(usuario = usuario , password = password).first()
    if user:
      self.notificacion.value = "Has iniciado sesión correctamente, Bienvenido!"
      self.notificacion.color = "green"
    else:
      self.notificacion.value = "Credenciales incorrectas"
      self.notificacion.color = "red"
    self.notificacion.update()
    
  def crear_usuario(self,e):
    usuario = self.entry_user.value
    password = self.entry_password.value
    cursor = Users(usuario = usuario, password = password)
    db.session.add(cursor)
    db.session.commit()
    self.notificacion.value = "Usuario creado correctamente."
    self.notificacion.color = "green"
    self.lbl_user.value = "Login"
    self.button_login.text = "Iniciar Sesión"
    self.button_login.on_click = self.verificar_credenciales
    self.page.update()


def main(page):
  page.title = "Login"
  page.vertical_alignment = ft.MainAxisAlignment.CENTER
  Login(page)

ft.app(target = main)