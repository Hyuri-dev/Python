import tkinter as tk
import ttkbootstrap as tkb
from ttkbootstrap.constants import * 
from tkinter import ttk
from database import create_user


class App :
    
    def __init__(self):
        self.root = tkb.Window(themename="superhero")
        self.root.title("Gestor de usuarios")
        
        
        #notebook
        self.pestañas = ttk.Notebook(self.root)
        
        #Contenido de las pestañas
        
        # Pestaña crear usuario
        self.pestaña_crear = tk.Frame(self.pestañas)
        
        #nombre entrada
        self.lbl_nombre = tk.Label(self.pestaña_crear, text="Nombre: ")
        self.lbl_nombre.grid(row= 0 , column= 0 ,pady= 20 )
        
        self.entry_nombre = tk.Entry(self.pestaña_crear)
        self.entry_nombre.grid(row= 0 , column=1)
        
        #Identificacion entrada
        self.lbl_identifiacion = tk.Label(self.pestaña_crear, text="Cedula/DNI: ")
        self.lbl_identifiacion.grid(row= 0 , column= 2, pady= 20)
        
        self.entry_identificacion = tk.Entry(self.pestaña_crear)
        self.entry_identificacion.grid(row= 0 , column= 3)
        
        #Botones crear y cancelar
        
        self.btn_crear = tkb.Button(self.pestaña_crear, text= "Crear", command= lambda: create_user(self) ,bootstyle = SUCCESS, width= 20)
        self.btn_crear.grid(row= 1 , column= 1, padx= (40 , 0) ,sticky="W")
        
        self.btn_cancelar = tkb.Button(self.pestaña_crear, text= "Cancelar", bootstyle = DANGER, width= 20)
        self.btn_cancelar.grid(row= 1 , column= 2, padx= (40 , 0) ,sticky="E")        
        
        
        self.relleno2 = ttk.Label(self.pestañas, text="")
        self.relleno3 = ttk.Label(self.pestañas, text="")
        
        
        #Agregar pestañas al notebook
        self.pestañas.add(self.pestaña_crear, text="Crear usuario")
        
        self.pestañas.pack()
        
        
        #Pestaña consultar usuario
        
        self.pestaña_consultar_usuario = tk.Frame(self.pestañas)
        self.lbl_consultar = tk.Label(self.pestaña_consultar_usuario, text= "Consultar usuario")
        self.lbl_consultar.grid(row= 0 , column= 0, padx=(220, 0), pady= 30)
        
        self.title_buscar = tk.Label(self.pestaña_consultar_usuario, text= "Identificacion (Cedula, RIF, DNI)")
        self.title_buscar.grid(row=1 , column= 0 )
        
        self.entry_busqueda_usuario = tk.Entry(self.pestaña_consultar_usuario)
        self.entry_busqueda_usuario.grid(row=1 , column=1)
        
        self.btn_buscar = tk.Button(self.pestaña_consultar_usuario, text="Buscar")
        self.btn_buscar.grid(row=1 , column= 2, padx=(20))
        
        
        self.pestañas.add(self.pestaña_consultar_usuario, text="Consulta de usuario")
        self.pestañas.add(self.relleno3, text="Lista de usuarios")
        
        
        self.root.mainloop()
        
        

App()