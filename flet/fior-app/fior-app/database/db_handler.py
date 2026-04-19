import sqlite3
import os


def get_connection ():
    # Creamos la carpeta database si no existe
    if not os.path.exists('database'):
        os.makedirs('database')


        # Conexion a la base de datos (se creara el archivo si no existe)
        conn = sqlite3.connect('database/db_fior')
        conn.row_factory = sqlite3.Row
        return conn

def create_tables ():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
CREATE TABLE IF NOT EXISTS productos (
                   id INTEGER PRIMARY KEY AUTOINCREMENT ,
                   nombre TEXT NOT NULL,
                   precio_base REAL NOT NULL,
                   foto_path TEXT )

''')
    
    cursor.execute('''
CREATE TABLE IF NOT EXISTS ventas (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   fecha DATETIME DEFAYKT CURRENT_TIMESTAMP,
                   referencia TEXT ,
                   total_venta REAL DEFAULT 0
                   )
''')
    
    cursor.execute('''
CREATE TABLE IF NOT EXISTS detalle_ventas(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   id_venta INTEGER  
                   id_producto INTEGER ,
                   cantidad INTEGER NOT NULL , 
                   precio_unitario REAL NOT NULL,
                   subtotal REAL NOT NULL,
                #    ON DELETE CASCADA para eliminar en cascada los datos relacionados si se elimina algun dato.
                   FOREIGN KEY (id_venta) REFERENCES ventas(id) ON DELETE CASCADE,
                   FOREIGN KEY (id_producto) REFERENCES productos(id),
                   )
''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Base de datos y tablas creadas exitosamente.")