import sqlite3 as lite3
import os
import ttkbootstrap as ttk
import tkinter as tk
import components.control_panel as cp
import components.treeview as tree



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
    return map_choferes



def data_window():
  #  configuracion del treeview
  
  columnas = ("id", "conductor", "vehiculo", 'placa')
  
  new_window = ttk.Toplevel(title="Datos")
  new_window.geometry("400x500")
  notebook = ttk.Notebook(new_window)
  notebook.pack(pady=3 , expand=True)
  
  tab_general = ttk.Frame(notebook, width=400 , height=500)
  tab_choferes = ttk.Frame(notebook, width= 400 , height=500)
  tab_vehiculos = ttk.Frame(notebook, width=400, height= 500)
  
  notebook.add(tab_general, text="General")
  notebook.add(tab_choferes, text="Choferes")
  notebook.add(tab_vehiculos, text="Vehiculos")
  
  
  
  btn_edit = ttk.Button(tab_general, text="Editar")
  
  FRAME_TREEVIEW = tk.Frame(tab_general, height= 200)
  FRAME_TREEVIEW.pack()
  
  
  
  treeview = ttk.Treeview(tab_general,columns=columnas, show='headings' , height=100)
  treeview.pack(expand=True, fill='both')
  
    
  treeview.heading('id', text="Id")
  treeview.heading('conductor',text="Conductor")
  treeview.heading('vehiculo',text="Camion Asignado")
  treeview.heading('placa', text="Placa")
  
  treeview.column('id',width=5, anchor="center")
  treeview.column('conductor',width=100, anchor="center")
  treeview.column('vehiculo',width=100, anchor="center")
  treeview.column('placa',width=100, anchor="center")
  
  for fila in treeview.get_children():
    treeview.delete(fila)
  
  
  cur = conexion.cursor()
  query = """
            SELECT c.id, c.name, v.name, v.car_plate
            FROM chofer c
            JOIN vehiculo v ON c.id_vehicle = v.id
        """
  cur.execute(query)
  resultados = cur.fetchall()
  for fila in resultados : 
    treeview.insert("", tk.END, values=fila)
    
    controles_general = cp.ControlPanel(
    FRAME_TREEVIEW, on_add=None,on_delete=None,on_edit=None)
    controles_general.pack(side="bottom", fill="x", pady=10)

  #  Vista para choferes
  
  columnas = ("id" , "conductor" , "vehiculo")
  
  FRAME_CHOFERES = ttk.Frame(tab_choferes, height=100)
  FRAME_CHOFERES.pack()
  W_MIN = int(400/len(columnas))
  
  treeview_choferes = ttk.Treeview(FRAME_CHOFERES,columns=columnas, show='headings' , height=10)
  treeview_choferes.pack(expand=True, fill='both', padx=10, pady=10)
  
    
  treeview_choferes.heading('id', text="Id")
  treeview_choferes.heading('conductor',text="Conductor")
  treeview_choferes.heading('vehiculo',text="Camion Asignado")

  
  treeview_choferes.column('id',width= W_MIN, anchor="center")
  treeview_choferes.column('conductor',width=W_MIN, anchor="center")
  treeview_choferes.column('vehiculo',width=W_MIN, anchor="center")
  
  for fila in treeview_choferes.get_children():
    treeview_choferes.delete(fila)
  
  
  cur = conexion.cursor()
  query = """
            SELECT c.id, c.name, v.name
            FROM chofer c
            JOIN vehiculo v ON c.id_vehicle = v.id
        """
  cur.execute(query)
  resultados = cur.fetchall()
  for fila in resultados : 
    treeview_choferes.insert("", tk.END, values=fila)
    
  
  controles_chofer = cp.ControlPanel(
    FRAME_CHOFERES, on_add=None,on_delete=None,on_edit=None
  )
  controles_chofer.pack(side="bottom", fill="x", pady=10)
  
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
  
  new_window.mainloop()



