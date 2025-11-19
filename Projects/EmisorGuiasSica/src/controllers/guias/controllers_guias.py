import sqlite3 as lite3
import os

map_choferes = {}

try:
  database = os.path.join(os.path.dirname(__file__), r"C:\Users\Personal\python\Python\Projects\EmisorGuiasSica\src\database\users.db") # 
  conexion = lite3.connect(database)
except lite3.OperationalError as e:
  print(f"Error al conectarse: {e}")


def llenar_combobox_chofer(conexiones , widget):
  cur = conexion.cursor()
  cur.execute("SELECT id, name FROM chofer")
  choferes = cur.fetchall()
  conexion.close()
  
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



