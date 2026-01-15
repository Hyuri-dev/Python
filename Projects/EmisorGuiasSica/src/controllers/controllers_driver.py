import tkinter as tk
import ttkbootstrap as ttkb
from tkinter import messagebox
import  sqlite3 as lite3
import os

try:
  database = os.path.join(os.path.dirname(__file__), r"C:\Users\Personal\python\Python\Projects\EmisorGuiasSica\src\database\users.db") # 
  conexion = lite3.connect(database)
except lite3.OperationalError as e:
  print(f"Error al conectarse: {e}")


def create_driver (name: str , cedula: int, vehiculo: int ,active: int):
  cur = conexion.cursor()
  cur.execute(f"INSERT INTO chofer (name , cedula, id_vehicle ,is_active) VALUES (?,?,?,?)", (name , cedula, vehiculo ,active))
  conexion.commit()
  messagebox.showinfo("Exito" , "Chofer creado exitosamente")



create_driver(name="Dave Laya" ,cedula=7184360 ,vehiculo=1, active=1)