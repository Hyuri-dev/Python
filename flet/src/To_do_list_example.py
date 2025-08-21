import flet as ft

def main (page: ft.Page):
  
  def add_clicked(e):
    page.add(ft.Checkbox(label = new_task.value))
    new_task.value = ""
    page.update()
    
  new_task = ft.TextField(hint_text = "Que necesitas hacer hoy ?", expand = True)
  tasks_views = ft.Column()
  view = ft.Column(
    width = 600,
    controls = [
      ft.Row (
        controls = [
          new_task, ft.FloatingActionButton(icon=ft.Icons.ADD, on_click = add_clicked),
        ],
      ),
      tasks_views,
    ],
  )
  page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
  page.add(view)
    
  # page.add(new_task, ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=add_clicked)) Esta era el boton viejo que salia debajo



ft.app(main)