import tkinter as tk
import ttkbootstrap as tkb
from tkinter import messagebox 
import sqlite3 as lite3
import os

try:
  database = os.path.join(os.path.dirname(__file__), "C:\\Users\\Jefferson\\desarrollo python\\hello_python\\Python\\Projects\\EmisorGuiasSica\\database\\company.db") # 
  conexion = lite3.connect(database)
except lite3.OperationalError as e:
  print(f"Error al conectarse: {e}")


def create_driver (name, lastname, cedula,is_active):
  cur = conexion.cursor()
  cur.execute("INSERT INTO chofer (name, lastname, cedula, is_active) VALUES (?,?,?,?)", (name,lastname,cedula, is_active,))
  conexion.commit()
  messagebox.showinfo("Solicitud", f"Se creo el conductor con los siguientes datos: {name , lastname , cedula} correctamente")


create_driver("Ahomi", "Carpio","28098234",1)
