import sqlite3 as lite3
import os
import ttkbootstrap as ttk
import tkinter as tk



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
  
  FRAME_TREEVIEW = ttk.Frame(tab_general, height= 200)
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

  #  Vista para choferes
  
  columnas = ("id" , "conductor" , "vehiculo")
  
  tframe_choferes = ttk.Treeview(tab_choferes, height=200)
  tframe_choferes.pack()
  W_MIN = int(400/3)
  
  treeview_choferes = ttk.Treeview(tframe_choferes,columns=columnas, show='headings' , height=100)
  treeview_choferes.pack(expand=True, fill='both')
  
    
  treeview_choferes.heading('id', text="Id")
  treeview_choferes.heading('conductor',text="Conductor")
  treeview_choferes.heading('vehiculo',text="Camion Asignado")
  # treeview_choferes.heading('placa', text="Placa")
  
  treeview_choferes.column('id',width= W_MIN, anchor="center")
  treeview_choferes.column('conductor',width=W_MIN, anchor="center")
  treeview_choferes.column('vehiculo',width=W_MIN, anchor="center")
  # treeview_choferes.column('placa',width=100, anchor="center")
  
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
  
  new_window.mainloop()


