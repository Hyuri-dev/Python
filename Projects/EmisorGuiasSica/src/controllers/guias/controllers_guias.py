import sqlite3 as lite3
import os
import ttkbootstrap as ttk
import tkinter as tk
import components.control_panel as cp
import components.treeview as tree
import controllers.controllers_driver as cd


map_choferes = {}
map_vehicles ={}

try:
  database = os.path.join(os.path.dirname(__file__), r"C:\Users\Personal\python\Python\Projects\EmisorGuiasSica\src\database\users.db") # 
  conexion = lite3.connect(database)
except lite3.OperationalError as e:
  print(f"Error al conectarse: {e}")


def llenar_combobox_chofer(conexiones , widget):
  cur = conexion.cursor()
  cur.execute("SELECT id, name FROM chofer")
  choferes = cur.fetchall()
  # conexion.close() Verificar este logout de la bd, no deja que cierre primero este y luego el segundo
  
  nombres =[]
  
  global map_choferes
  map_choferes = {}
  
  for chofer in choferes:
    id_db = chofer[0]
    nombre_db = chofer[1]
    map_choferes[nombre_db] = id_db
    nombres.append(nombre_db)
    
    
  widget['values']= nombres
  return map_choferes

def  llenar_combobox_vehiculo (conexiones, widget):
  cur = conexion.cursor()
  cur.execute("SELECT id , name FROM vehiculo ")
  vehiculos = cur.fetchall()
  # conexion.close()
  
  nombres = []
  
  global map_vehicles
  map_vehicles = {}
  
  for vehiculo in vehiculos:
    id_db = vehiculo[0]
    nombre_db = vehiculo[1]
    map_vehicles[nombre_db] = id_db
    nombres.append(nombre_db)
    
    widget['values'] = nombres
  return map_vehicles



def data_window():
  #  configuracion del treeview
  
  columnas = ("id", "conductor", "vehiculo", 'placa')
  
  new_window = ttk.Toplevel(title="Datos")
  new_window.geometry("400x500")
  notebook = ttk.Notebook(new_window, height=500)
  notebook.pack(side="top",pady=3 , expand=True)
  
  tab_general = ttk.Frame(notebook, width=400 , height=500)
  tab_choferes = ttk.Frame(notebook, width= 400 , height=500)
  tab_vehiculos = ttk.Frame(notebook, width=400, height= 500)
  
  notebook.add(tab_general, text="General")
  notebook.add(tab_choferes, text="Choferes")
  notebook.add(tab_vehiculos, text="Vehiculos")
  
  
  FRAME_GENERAL = tk.Frame(tab_general, height= 200)
  FRAME_GENERAL.pack()
  
  cols = ("id" , "conductor" , "vehiculo", "placa")
  headers = ("ID" , "Nombre", "Camión Asignado", "Placa")
  widths = (50, 100 ,100, 100)
  
  tabla_general = tree.VistaListado(FRAME_GENERAL,cols, headers, widths)
  tabla_general.pack(side="top", fill="both", expand=True)
  
  cur = conexion.cursor()
  query = """
            SELECT c.id, c.name, v.name, v.car_plate
            FROM chofer c
            JOIN vehiculo v ON c.id_vehicle = v.id
        """
  cur.execute(query)
  tabla_general.cargar_datos(cur.fetchall())
    
  controles_general = cp.ControlPanel(
    FRAME_GENERAL, on_add=None,on_delete=None,on_edit=None)
  
  controles_general.pack()
  
  #  Vista para choferes
  
  FRAME_CHOFERES = ttk.Frame(tab_choferes, height=100)
  FRAME_CHOFERES.pack()
  
  cols = ("id" , "conductor" , "vehiculo")
  headers = ("ID" , "Nombre", "Camión Asignado")
  widths = (116 , 116 ,116)
  
  tabla_choferes = tree.VistaListado(FRAME_CHOFERES,columnas=cols, encabezados=headers, anchos=widths)
  tabla_choferes.pack(side="top", fill="both", expand=True)


  query = """
            SELECT c.id, c.name, v.name
            FROM chofer c
            JOIN vehiculo v ON c.id_vehicle = v.id
        """
  cur.execute(query)
  tabla_choferes.cargar_datos(cur.fetchall())
  
  
  controles_chofer = cp.ControlPanel(
    FRAME_CHOFERES, on_add=cd.create_driver,on_delete=None,on_edit=None
  )
  controles_chofer.pack()

  # Sección de vehiculos
  
  FRAME_VEHICULOS = ttk.Frame(tab_vehiculos, height=100)
  FRAME_VEHICULOS.pack()
  
  cols = ("id", "nombre","placa", "tipo")
  headers = ("ID","Nombre","Placa","Tipo")
  widths = (50,100,100,100)
  
  tabla_vehiculos = tree.VistaListado(FRAME_VEHICULOS, cols, headers,widths)
  tabla_vehiculos.pack(side="top", fill="both", expand=True)
  query = """
    SELECT v.id, v.name, v.car_plate, tv.name 
    FROM vehiculo v 
    JOIN tipo_vehiculo tv ON v.id_type_vehicle = tv.id 
"""
  cur.execute(query)
  tabla_vehiculos.cargar_datos(cur.fetchall())
  
  controles_vehiculo = cp.ControlPanel(FRAME_VEHICULOS)
  controles_vehiculo.pack()
  
  new_window.mainloop()



