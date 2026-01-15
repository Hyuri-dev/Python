import tkinter as tk
import ttkbootstrap as tkb
from tkinter import messagebox 
import sqlite3 as lite3
import os

try:
  database = os.path.join(os.path.dirname(__file__), r"C:\Users\Personal\python\Python\Projects\EmisorGuiasSica\src\database\users.db")
  conexion = lite3.connect(database)
except lite3.OperationalError as e:
  print(f"Error al conectarse: {e}")

def crear_vehiculo (nombre, placa ,tipo_vehiculo):
  cur = conexion.cursor()
  cur.execute("INSERT INTO vehiculo (name, car_plate, id_type_vehicle) VALUES (?,?,?)", (nombre, placa ,tipo_vehiculo,))
  conexion.commit()
  messagebox.showinfo("Solicitud",f"Se ha creado el vehiculo: {nombre} con placa: {placa} correctamente")


crear_vehiculo(nombre="A15" , placa="A15BS9D", tipo_vehiculo="1")