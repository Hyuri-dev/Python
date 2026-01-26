import tkinter as tk
import ttkbootstrap as ttkb
from tkinter import messagebox
import  sqlite3 as lite3
import os
import controllers.guias.controllers_guias as cg
import components.control_panel as cp


try:
  database = os.path.join(os.path.dirname(__file__), r"C:\Users\Personal\python\Python\Projects\EmisorGuiasSica\src\database\users.db") # 
  conexion = lite3.connect(database)
except lite3.OperationalError as e:
  print(f"Error al conectarse: {e}")


def create_driver ():
  
  def crear():
    from controllers.guias.controllers_guias import map_vehicles
    active = 1
    
    name_selected = lista_vehiculo.get()
    id_vehicle = map_vehicles.get(name_selected)
    
    if not id_vehicle:
      messagebox.showwarning("Advertencia", "Por favor, Seleccione un vehiculo")
      return
    
    cur = conexion.cursor()
    cur.execute("INSERT INTO chofer (name , cedula, id_vehicle ,is_active) VALUES (?,?,?,?)", (input_name.get(), input_cedula.get(), id_vehicle, active))
    conexion.commit()
    messagebox.showinfo("Exito" , "Chofer creado exitosamente")
    window.destroy()

  def editar ():
  window = ttkb.Toplevel(title="Creación de Chofer")
  window.geometry("300x400")
  
  label_frame_chofer = ttkb.Labelframe(window, text="Datos del Chofer", bootstyle="primary", padding= 5 , width=300)
  label_frame_chofer.pack(pady=2, padx= 10)
  
  label_chofer = ttkb.Label(label_frame_chofer, text="Nombre", width=300, bootstyle="dark")
  label_chofer.pack(pady=10, fill="x")
  
  input_name = ttkb.Entry(label_frame_chofer)
  input_name.pack(pady=5, fill="x")
  
  label_cedula = ttkb.Label(label_frame_chofer, text="Cedula", bootstyle="dark")
  label_cedula.pack(pady=(5,2) , fill="x")
  
  input_cedula = ttkb.Entry(label_frame_chofer)
  input_cedula.pack(pady=5, fill="x")
  
  label_vehiculo_asignado = ttkb.Label(label_frame_chofer, text="Vehiculo a Asignar", bootstyle="dark")
  label_vehiculo_asignado.pack(pady=(5,2) , fill="x")
  
  lista_vehiculo = ttkb.Combobox(label_frame_chofer, state="readonly")
  lista_vehiculo.pack(pady=(5,9), fill="x")
  
  cg.llenar_combobox_vehiculo(conexion, lista_vehiculo, )
  
  # Solucionar el listado: esta devolviendo el nombre del camión en vez del id a la hora de insertarlo en la BD
  
  botones = cp.ButtonsBasic(label_frame_chofer,cancel=None , on_add=crear)
  botones.pack()
  

  
  
  
  
  
  window.mainloop()
  




# create_driver(name="Dave Laya" ,cedula=7184360 ,vehiculo=1, active=1)