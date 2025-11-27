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


def create_vehicle (name, car_plate, id_type):
  cur = conexion.cursor()
  cur.execute("INSERT INTO vehiculo (name, car_plate, id_type_vehicle) VALUES (?,?,?)", (name,car_plate,id_type,))
  conexion.commit()
  messagebox.showinfo("Solicitud", f"Se creo el vehiculo: {name} con placa: {car_plate} correctamente")


create_vehicle("A15", "A7A6SD", 1)
