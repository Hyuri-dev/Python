import sqlite3 as lite3
import tkinter as tk
from tkinter import messagebox 
import os


database = os.path.join(os.path.dirname(__file__), "users.db") # Ruta relativa de nuestra BD

conexion = lite3.connect(database)

try:
  conexion.execute(""" CREATE TABLE IF NOT EXISTS usuarios (
    id integer primary key autoincrement , nombre text, cedula integer unique)""")
  
  # print("tabla creada con exito")
except lite3.OperationalError as e:
  print(f"Error no se ha podido hacer tu solicitud: {e}")
  
  
def create_user(app):
  cur = conexion.cursor()
  cur.execute("INSERT INTO usuarios (nombre , cedula) VALUES(?,?)",(app.entry_nombre.get(), app.entry_identificacion.get()))
  conexion.commit()
  # app.entry_nombre.get(0, tk.END) añadir este reseteo de entry
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

