import tkinter as tk
import ttkbootstrap as tkb
from ttkbootstrap.constants import * 
from tkinter import ttk
from database import create_user , search_user, mostrar_usuarios , obtener_item , eliminar_usuario, actualizar_usuario


class App :
    
    def __init__(self):
        self.root = tkb.Window(themename="superhero")
        self.root.title("Gestor de usuarios")
        self.root.resizable(False, False)
        
        
        #notebook
        self.pestañas = ttk.Notebook(self.root)
        
        #Contenido de las pestañas
        
        # Pestaña crear usuario
        self.pestaña_crear = tk.Frame(self.pestañas)
        self.pestaña_crear.grid_columnconfigure(0 , weight= 1)
        self.pestaña_crear.grid_columnconfigure(1 , weight= 1)
        self.pestaña_crear.grid_columnconfigure(2 , weight= 1)
        
        
        self.title_crear = tk.Label(self.pestaña_crear,text="Creación de usuario")
        self.title_crear.grid(row= 0 , column= 0, columnspan= 3, sticky= "ew", pady= (30, 20), padx=(145 ,20))
        self.title_crear.config(font=("Arial", 18, "bold"), fg= "#5597DD", anchor= "center", justify= "center")
        
        #nombre entrada
        self.lbl_nombre = tk.Label(self.pestaña_crear, text="Nombre: ")
        self.lbl_nombre.grid(row= 1 , column= 0 ,pady= 20 )
        
        self.entry_nombre = tk.Entry(self.pestaña_crear)
        self.entry_nombre.grid(row= 1 , column=1)
        
        #Identificacion entrada
        self.lbl_identifiacion = tk.Label(self.pestaña_crear, text="Cedula/DNI: ")
        self.lbl_identifiacion.grid(row= 1 , column= 2, pady= 20)
        
        self.entry_identificacion = tk.Entry(self.pestaña_crear)
        self.entry_identificacion.grid(row= 1 , column= 3)
        
        #Botones crear y cancelar
        
        self.btn_crear = tkb.Button(self.pestaña_crear, text= "Crear", command= lambda: create_user(self) ,bootstyle = SUCCESS, width= 20)
        self.btn_crear.grid(row= 2 , column= 1, padx= (40 , 0) ,pady=(30, 0),sticky="W")
        
        self.btn_cancelar = tkb.Button(self.pestaña_crear, text= "Cancelar", bootstyle = DANGER, width= 20)
        self.btn_cancelar.grid(row= 2 , column= 2, padx= (40 , 0),pady=(30 ,0) ,sticky="E")        
        
        
        #Agregar pestañas al notebook
        self.pestañas.add(self.pestaña_crear, text="Crear usuario")
        
        self.pestañas.pack()
        
        
        #Pestaña consultar usuario
        
        # Modificamos las columnas para que abarquen todo el espacio en base a su peso
        self.pestaña_consultar_usuario = tk.Frame(self.pestañas)
        self.pestaña_consultar_usuario.grid_columnconfigure(0 , weight= 1)
        self.pestaña_consultar_usuario.grid_columnconfigure(1 , weight= 1)
        self.pestaña_consultar_usuario.grid_columnconfigure(2 , weight= 1)
        
        # Titulos
        self.lbl_consultar = tk.Label(self.pestaña_consultar_usuario, text= "Consultar usuario")
        self.lbl_consultar.grid(row= 0 , column= 0,columnspan= 3, pady= 30, sticky="ew")
        self.lbl_consultar.config(font=("Arial", 16, "bold"))
        
        self.title_buscar = tk.Label(self.pestaña_consultar_usuario, text= "Identificacion (Cedula, RIF, DNI)")
        self.title_buscar.grid(row=1 , column= 0 , sticky="W")
        
        # Entry's (inputs)
        self.entry_busqueda_usuario = tk.Entry(self.pestaña_consultar_usuario)
        self.entry_busqueda_usuario.grid(row=1 , column=0, padx= (110, 10))
        
        #Boton buscar usuario 
        self.btn_buscar = tk.Button(self.pestaña_consultar_usuario, text="Buscar", command= lambda: search_user(self))
        self.btn_buscar.grid(row=1 , column= 0, padx= (290, 10))
        
        # Output para la busqueda, esto reotrna o mostrara el usuario ingresado con sus datos si existe
        self.text_user = tk.Label(self.pestaña_consultar_usuario, text= f"Usuario: ")
        self.text_user.grid(row= 2 , column= 0, sticky= "W", padx= 15 ,pady= (30, 0))
        self.text_user.config(font=("Arial" , 14 , "bold"))
        
        
        self.pestañas.add(self.pestaña_consultar_usuario, text="Consulta de usuario")
        
        
        
        #Listado de usuarios
        
        
        self.pestaña_listado_usuarios = tk.Frame (self.pestañas)
        self.pestaña_listado_usuarios.grid_columnconfigure(0, weight= 1)
        self.pestaña_listado_usuarios.grid_columnconfigure(1, weight= 1)
        self.pestaña_listado_usuarios.grid_columnconfigure(2, weight= 1)
        
        
        
        self.title_listado = tk.Label(self.pestaña_listado_usuarios, text="Listado de usuarios registrados")
        self.title_listado.grid(row= 0 , column= 0, columnspan= 3 , sticky="ew", pady= 20)
        self.title_listado.config(font=("Arial", 16 , "bold"))
        
        self.button_edit = tkb.Button(self.pestaña_listado_usuarios, text="Editar", command= lambda: actualizar_usuario(self), bootstyle = WARNING)
        self.button_edit.grid(row= 1 , column=0, sticky="ew" , pady= (15, 15), padx=(80, 20))

        self.button_eliminar = tkb.Button (self.pestaña_listado_usuarios, text="Eliminar" , command= lambda: eliminar_usuario(self), bootstyle= SUCCESS)
        self.button_eliminar.grid (row= 1, column=1, sticky="we" , pady= (15, 15), padx=(150, 20))
        
        
        
        #Treeview
        self.treeview_usuarios = ttk.Treeview(self.pestaña_listado_usuarios)
        self.treeview_usuarios.grid(row= 2 , column= 0 , columnspan= 3, sticky="ew ")
        
        #Establecemos las cabeceras o columnas
        self.treeview_usuarios["columns"] = ("1" , "2" , "3")
        self.treeview_usuarios["show"] = "headings"
        
        #ancho del treeview
        self.treeview_usuarios.column("1", width= 30, anchor="center")
        self.treeview_usuarios.column("2", width= 200, anchor="center")
        self.treeview_usuarios.column("3", width= 200, anchor="center")
        
        
        #Cabeceras con sus titulos para el treeview
        self.treeview_usuarios.heading("1",text= "ID")
        self.treeview_usuarios.heading("2",text= "Usuario")
        self.treeview_usuarios.heading("3",text= "Cedula")
        
        #añadiomos la hoja al notebook
        self.pestañas.add(self.pestaña_listado_usuarios, text="Lista de usuarios")
        
        mostrar_usuarios(self)
        self.root.mainloop()
        
        

App()