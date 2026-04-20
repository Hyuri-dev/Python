from src.db.db_handler import get_connection

def add_product(name , price , image_path=None):
    """INSERTA UN NUEVO PRODUCTO EN LA BASE DE DATOS."""
    conn = get_connection()
    if conn: 
        try:
            cursor = conn.cursor()
            query = "INSERT INTO productos (nombre,precio_base,foto_path) VALUES (? ,? ,?)"
            cursor.execute(query,(name, price, image_path))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al agregar producto: {e}")
            return False
        finally:
            conn.close()
    return False

def get_products():
    """"OBTIENE UN LISTADO DE TODOS LOS PRODUCTOS """

    conn = get_connection()
    productos = []
    if conn:
        try: 
            cursor = conn.cursor()
            cursor.execute("SELECT * from productos")
            productos = [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error al obtener productos: {e}")
        finally:
            conn.close()
    return productos


def delete_products(id_product):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM productos WHERE id = ?", (id_product,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar: {e}")
            return False
        finally:
            conn.close()
    return False