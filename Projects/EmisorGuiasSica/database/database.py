import sqlite3 as lite3
import os


try:
  database = os.path.join(os.path.dirname(__file__), "company.db") # Ruta relativa de nuestra BD

  conexion = lite3.connect(database)
  conexion.execute("PRAGMA foreign_keys = ON;")
except lite3.Error as e:
  print(f"Ocurrio un error de sqlite: {e}")

def crear_tablas():
  try:
    conexion.execute(""" CREATE TABLE IF NOT EXISTS chofer (
      id integer primary key autoincrement,
                     name text not null,
                      lastname text not null, 
                      cedula integer unique not null,
                      is_active integer not null default 1 CHECK (is_active IN (0,1)));""")
    
    conexion.execute("""CREATE TABLE IF NOT EXISTS tipo_vehiculo (
        id integer primary key autoincrement
        , name text not null unique);""")
    
    conexion.execute("""CREATE TABLE IF NOT EXISTS vehiculo (
        id integer primary key autoincrement, 
        name text not null, 
        car_plate string not null,
        id_type_vehicle int not null,
        FOREIGN KEY(id_type_vehicle) REFERENCES tipo_vehiculo(id))""")
    
    conexion.commit()
    print("Tablas creadas correctamente")
  except lite3.OperationalError as e:
    print(f"Error no se ha podido hacer tu solicitud: {e}")

crear_tablas()