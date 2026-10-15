import flet as ft
import script



def main(page: ft.Page):
    tasa = script.obtener_bcv()
    result = ft.Text(value = f"este es un resultado de la tasa {tasa}")
    page.add(ft.Text(value="Hello world"),result)
  


if __name__ == "__main__":
    ft.run(main)
