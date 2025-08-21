import flet as ft

# los widgets se añaden a la pagina y asi se iran renderizando, como este texto.
def main (page: ft.Page):
  page.add(ft.Text(value = " Hello Flet ! "))

ft.app(main)
