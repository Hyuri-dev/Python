import sqlite3
import os


def get_connection ():
    # Creamos la carpeta database si no existe
    try:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        db_dir = os.path.join(base_dir, 'database')
        os.makedirs(db_dir, exist_ok=True)

        db_path = os.path.join(db_dir, 'db_fior.db')

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None
        
    # if not os.path.exists('database'):
    #     os.makedirs('database')
        # Conexion a la base de datos (se creara el archivo si no existe)

def create_tables ():
    conn = get_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio_base REAL NOT NULL,
    foto_path TEXT
)

''')
            
            cursor.execute('''
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    referencia TEXT,
    total_venta REAL DEFAULT 0
)

''')
            
            cursor.execute('''
CREATE TABLE IF NOT EXISTS detalle_ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_venta INTEGER,
    id_producto INTEGER,
    cantidad INTEGER NOT NULL,
    precio_unitario REAL NOT NULL,
    subtotal REAL NOT NULL,
    FOREIGN KEY (id_venta) REFERENCES ventas(id) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES productos(id)
)

''')
            
            conn.commit()
            print("Base de datos y tablas creadas exitosamente.")
        except Exception as e:
            print(f"Error al crear las tablas {e}")
        finally:
            conn.close()
    else:
        print("No se pudo establecer la conexion para crear las tablas.")

if __name__ == "__main__":
    create_tables()
