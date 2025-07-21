"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config


class State(rx.State):
    
    user = {"usuario" : "aquiles",
            "contraseña": "admin"}
    usuario = ""
    contrasena = ""
    text: str = ""
    error: str  = ""
    
    def validar (self):
        if self.usuario == self.user["usuario"] and self.contrasena == self.user["contraseña"]:
            self.text = "Login exitoso, Bienvenido!"
        else:
            self.text = "Usuario o contraseña mal ingresado, intente nuevamente"

#Crear el formulario de login


def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Login",size="9" ,color_scheme= "blue"),
            rx.heading("Usuario", size= "4", margin_top= "1em"),
            rx.input(placeholder="@aquiles", value=State.usuario ,on_change=State.set_usuario),
            rx.heading("Contraseña", size="4", margin_top= "1em"),
            rx.input(placeholder="**************", value= State.contrasena ,on_change=State.set_contrasena),
            rx.hstack(
                rx.button("Ingresar", color_scheme="green" ,on_click= State.validar),
                rx.text(State.text)
            ),
        ),
    )


app = rx.App()
app.add_page(index)
