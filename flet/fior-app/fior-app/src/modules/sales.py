from src.db.db_handler import get_connection

def add_sale(ref, details_car):
    """"Registra una venta"""

    conn = get_connection()
    if not conn: 
        return False
    
    try:
        cursor = conn.cursor()

        total_sale = sum(item['cantidad']*item['precio_unitario'] for item in details_car)

        cursor.execute("INSERT INTO ventas (referencia, total_venta) VALUES (?,?)",(ref,total_sale))

        id_sale = cursor.lastrowid

        for item in details_car:
            subtotal = item['cantidad'] * item['precio_unitario']
            cursor.execute(''' 
INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, precio_unitario, subtotal) VALUES (?,?,?,?,?)
''', (id_sale, item['id_producto'], item['cantidad'], item['precio_unitario'], subtotal))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al registrar la venta: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def get_resumen():
    conn = get_connection()
    if not conn:
        return {"Total_dinero": 0 , "cantidad_ventas":0}
    
    try:
        cursor = conn.cursor()
        cursor.execute('''
SELECT count(id) as cantidad_ventas, SUM (total_venta) as total_dinero FROM VENTAS WHERE date(fecha, 'localtime') = date('now', 'localtime')
''')
        resultado = dict(cursor.fetchone())

        if resultado['total_dinero'] is None:
            resultado['total_dinero'] = 0

        return resultado 
    except Exception as e: 
        print(f"Error al obtener resumen: {e}")
        return {"total_dinero": 0 , "cantidad_ventas":0}
    finally:
        conn.close()

