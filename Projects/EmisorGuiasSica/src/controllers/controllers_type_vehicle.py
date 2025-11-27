import tkinter as tk
import ttkbootstrap as tkb
from tkinter import messagebox 
import sqlite3 as lite3
import os

try:
<<<<<<< HEAD:Projects/EmisorGuiasSica/src/controllers/controllers_type_vehicle.py
  database = os.path.join(os.path.dirname(__file__), r"C:\Users\Personal\python\Python\Projects\EmisorGuiasSica\src\database\users.db")
=======
  database = os.path.join(os.path.dirname(__file__), "C:\\Users\\Jefferson\\desarrollo python\\hello_python\\Python\\Projects\\EmisorGuiasSica\\database\\company.db") # 
>>>>>>> afd9939026ba5bee4c96f4d9df4b50ed9e2866d2:Projects/EmisorGuiasSica/controllers/controllers_type_vehicle.py
  conexion = lite3.connect(database)
except lite3.OperationalError as e:
  print(f"Error al conectarse: {e}")


def create_type_vehicle (name):
  cur = conexion.cursor()
<<<<<<< HEAD:Projects/EmisorGuiasSica/src/controllers/controllers_type_vehicle.py
  cur.execute(f"INSERT INTO tipo_vehiculo (name) VALUES (?)", (name,))
=======
  cur.execute("INSERT INTO tipo_vehiculo (name) VALUES (?)", (name,))
>>>>>>> afd9939026ba5bee4c96f4d9df4b50ed9e2866d2:Projects/EmisorGuiasSica/controllers/controllers_type_vehicle.py
  conexion.commit()
  messagebox.showinfo("Solicitud", f"Se creo el tipo de vehiculo:{name} correctamente")




create_type_vehicle("Sedan")