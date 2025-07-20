import sqlite3 as lite3
import tkinter as tk
import ttkbootstrap as tkb
from ttkbootstrap.constants import * 
from tkinter import messagebox 
import os


database = os.path.join(os.path.dirname(__file__), "users.db") # Ruta relativa de nuestra BD

conexion = lite3.connect(database)

try:
  conexion.execute(""" CREATE TABLE IF NOT EXISTS usuarios (
    id integer primary key autoincrement , nombre text, cedula integer unique)""")
except lite3.OperationalError as e:
  print(f"Error no se ha podido hacer tu solicitud: {e}")
  
  
def create_user(app):
  cur = conexion.cursor()
  cur.execute("INSERT INTO usuarios (nombre , cedula) VALUES(?,?)",(app.entry_nombre.get(), app.entry_identificacion.get()))
  conexion.commit()
  messagebox.showinfo("Solicitud", "Usuario creado con exito")
  mostrar_usuarios(app)
  app.entry_nombre.delete(0, tk.END)
  app.entry_identificacion.delete(0, tk.END)

def search_user(app):
  buscador = app.entry_busqueda_usuario.get()
  cur = conexion.cursor()
  cur.execute(f"SELECT * FROM usuarios WHERE cedula = ?", (buscador,))
  resultado = cur.fetchone()
  
  if resultado:
    nombre = resultado[1]
    cedula = str(resultado[2])
    texto = f"Usuario: {nombre} {cedula}"
    app.entry_busqueda_usuario.delete(0, tk.END)
  else:
    texto = "Usuario no encontrado"
    
  app.text_user.config(text= texto)
  conexion.commit()


def mostrar_usuarios (app):
  cur = conexion.cursor()
  cur.execute("SELECT * FROM usuarios ")
  resultado = cur.fetchall()
  
  for item in app.treeview_usuarios.get_children():
    app.treeview_usuarios.delete(item)
  
  #insertar usuarios 
  
  for fila in resultado:
    app.treeview_usuarios.insert("", "end", values=(fila[0], fila[1], fila[2]))

def obtener_item (app):
  selected_item = app.treeview_usuarios.selection() # usamos tree selection para seleccionar el item que queremos manipular
  
  if selected_item:
    messagebox.showinfo("Seleccion", f"Se selecciono el item: {selected_item} correctamente")
    # print(f"Se selecciono el item: {selected_item}")

def eliminar_usuario (app):
  selected_item = app.treeview_usuarios.selection() # usamos tree selection para seleccionar el item que queremos manipular
  if selected_item: 
    valores = app.treeview_usuarios.item(selected_item[0], "values")
    id_usuario = valores[0]
    cur = conexion.cursor()
    cur.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
    conexion.commit()
    mostrar_usuarios(app)
    messagebox.showinfo("Eliminado", f"Usuario con ID: {id_usuario} eliminado correctamente")
  else:
    messagebox.showerror("Error", "No se ha podido eliminar el usuario")

def actualizar_usuario (app):
  selected_item = app.treeview_usuarios.selection()
  if selected_item:
    valores = app.treeview_usuarios.item(selected_item[0], "values")
    id = valores[0]
    nombre = valores[1]
    cedula = valores[2]
    

    
    top = tk.Toplevel()
    top.geometry("550x220")
    top.title("Editar usuario")
    
    top.grid_columnconfigure(0, weight= 1)
    top.grid_columnconfigure(1, weight= 1)
    top.grid_columnconfigure(2, weight= 1)
    
    title = tk.Label(top, text= "Editar Usuario")
    title.grid(row= 0 , column= 0, columnspan= 3 , sticky= "ew", pady=(25,20))
    title.config(font=("Arial", 16,"bold"), fg="#5597DD")
    
    
    lbl_nombre = tk.Label(top,text="Nombre: ")
    lbl_nombre.grid(row= 1 , column= 0 ,columnspan= 3 ,sticky="w", padx= 20)
    
    entry_nombre = tk.Entry(top)
    entry_nombre.insert(tk.END, f"{nombre}")
    entry_nombre.grid(row=1 , column= 0 , padx=(90,0))
    
    lbl_identificacion = tk.Label(top, text= "Identificacion: ")
    lbl_identificacion.grid(row= 1 , column= 1, columnspan= 1 , sticky="w", padx=(50, 0))
    
    entry_identificacion = tk.Entry (top)
    entry_identificacion.insert(tk.END,f"{cedula}")
    entry_identificacion.grid( row= 1, column= 2 )
    
    btn_guardar = tkb.Button(top, text="Guardar",command= lambda: editar() ,bootstyle = SUCCESS)
    btn_guardar.grid(row= 2 , column= 0,columnspan= 3 ,sticky="ew", pady= (10 , 10), padx= 10)
    
    btn_cancelar = tkb.Button (top, text= "Cancelar" , command= lambda: destruir_top(), bootstyle = DANGER)
    btn_cancelar.grid (row= 3 , column= 0 ,columnspan= 3 ,sticky="ew", pady= 10, padx= 10)
    
    def editar ():
      cur = conexion.cursor()
      cur.execute(f"UPDATE usuarios SET nombre = ? , cedula = ? WHERE ID = {id}", (entry_nombre.get() ,entry_identificacion.get(),))
      conexion.commit()
      messagebox.showinfo("Editar usuario", f"Se ha editado el usuario con ID: {id} correctamente")
      top.destroy()
      mostrar_usuarios(app)
    
    def destruir_top ():
      top.destroy()
  else:
    messagebox.showerror("Error", "Debe seleccionar un usuario para poder actualizar los datos")

