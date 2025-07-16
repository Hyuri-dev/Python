import sqlite3 as lite3
import tkinter as tk

conexion = lite3.connect("C:\\Users\\Personal\\code\\python\\Python\\hello_python\\crud\\users.db")

try:
  conexion.execute(""" CREATE TABLE IF NOT EXISTS usuarios (
    id integer auto increment, nombre text, cedula integer primary key)""")
  
  # print("tabla creada con exito")
except lite3.OperationalError as e:
  print(f"Error no se ha podido hacer tu solicitud: {e}")
  
  
def create_user(app):
  cur = conexion.cursor()
  cur.execute("INSERT INTO usuarios (nombre , cedula) VALUES(?,?)",(app.entry_nombre.get(), app.entry_identificacion.get()))
  conexion.commit()
  # app.entry_nombre.get(0, tk.END) añadir este reseteo de entry
  print(f"creado con exito")
  conexion.close()
