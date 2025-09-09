import flet as ft

class myApp(ft.Column):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.vista_productos = ft.Column(scroll=ft.ScrollMode.ALWAYS, height= 800, width= 500)
        self.width = 900
        
        # Widgets
        self.text_bar = ft.TextField(hint_text="  Buscar un producto " , border_radius=30, border_color="#b9e3ff")
        self.button_create = ft.FilledButton(
            text="Crear Producto", 
            on_click=lambda e: self.page.open(self.dlg), 
            icon_color="",
            icon=ft.Icons.ADD_OUTLINED, 
            bgcolor='#02B431',
            color='#ffffff'
        )
        
        #Widgets para la Modal crear productos
        self.input_producto = ft.TextField(label="🏷️Nombre", width= 300)
        self.input_precio = ft.TextField(label="💲Precio")
        self.input_categoria = ft.TextField(label="🗂️Categoria")
        self.input_peso = ft.TextField(label="⚖️Peso")
        self.input_ubicacion = ft.TextField(label="📍Ubicacion")
        
        self.mensaje = ft.Text("", color="#02B431")        
        self.dlg = ft.AlertDialog(
            title="Crear un producto 📦",
            content= ft.Column(
                [
                    self.input_producto,
                    self.input_precio,
                    self.input_categoria,
                    self.input_peso,
                    self.input_ubicacion,
                    ft.ElevatedButton("Crear Producto", on_click=self.crear_producto),
                    ft.ElevatedButton("Limpiar Formulario", icon=ft.Icons.DELETE, on_click=self.limpiar_campos_producto),
                    self.mensaje
                    
                ],
            width= 250, height=400),
            alignment= ft.alignment.center
        )
        self.dlg_edit = ft.AlertDialog(
            title ="Editar producto✍️",
            content= ft.Column(
                [
                    self.input_producto,
                    self.input_precio,
                    self.input_categoria,
                    self.input_peso,
                    self.input_ubicacion,
                    ft.ElevatedButton("Editar Producto", on_click=self.crear_producto),
                    ft.ElevatedButton("Limpiar Formulario", icon=ft.Icons.DELETE, on_click=self.limpiar_campos_producto),
                    self.mensaje
                ])
        )
        self.controls = [
            ft.Row(controls=[self.text_bar, self.button_create]),
            ft.Container(
                content=self.vista_productos,
                bgcolor="#2b2b2b",
                width= 1200,
                height=900,
                border_radius= 22,
                alignment=ft.alignment.center,
                margin= ft.margin.only(top= 30),
                padding= ft.padding.only(left= 40, right=10, top= 10 , bottom= 10),
                expand=True
                ),
                
            
            
        ]

    # ----- METODOS -----
    
    def mostrar_mensaje(self,e):
        mensaje = self.input_dialog.value
        self.mensaje.value = mensaje
        self.page.update()
        
    
    
    def crear_producto(self, e):
        # Aquí usas los valores de los campos para crear el producto
        producto = self.input_producto.value  # Ejemplo: obtener el texto del campo
        precio = self.input_precio.value
        categoria = self.input_categoria.value
        peso = self.input_peso.value
        ubicacion = self.input_ubicacion.value
        self.mensaje.value = "Producto creado e ingresado con exito!"
        
        # Lógica para agregar el producto a la vista
        self.vista_productos.controls.append( ft.Row(
            controls=[
                ft.Text(f"{producto}  {precio}  {categoria}  {peso}  {ubicacion}", size= 25),
                ft.IconButton(icon=ft.Icons.CREATE_OUTLINED, on_click =lambda e:self.page.open(self.dlg_edit)), 
                ft.IconButton(icon=ft.Icons.DELETE_OUTLINE_ROUNDED)
            ]
        )
        )
        
        self.input_producto.value =""
        self.update()  # Actualiza la interfaz
    
    def limpiar_campos_producto(self, e):
        self.input_producto.value = ""
        self.input_precio.value = ""
        self.input_categoria.value = ""
        self.input_peso.value = ""
        self.input_ubicacion.value = ""
        self.page.update()

def main(page: ft.Page):
    page.title = "Manejador de precios"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    app = myApp(page)  # Solo pasamos 'page' como argumento
    page.add(app)
    page.update()

ft.app(target=main)


