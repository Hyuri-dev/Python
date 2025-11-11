import tkinter as tk
import ttkbootstrap as tkb
from tkinter import messagebox 
import sqlite3 as lite3
import os

try:
  database = os.path.join(os.path.dirname(__file__), "users.db") # 
  conexion = lite3.connect(database)
except lite3.OperationalError as e:
  print(f"Error al conectarse: {e}")


def create_type_vehicle (name):
  cur = conexion.cursor()
  cur.execute(f"INSERT INTO tipo_vehiculo (name) VALUES (?)", (name))
  conexion.commit()
  messagebox.showinfo(f"Solicitud", "Se creo el tipo de vehiculo:{name} correctamente")




# create_type_vehicle("Sedan")