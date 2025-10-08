import mariadb
import sys

def conectar ():
        try:
            conexion = mariadb.connect(
                host="147.135.104.21",
                user="jodomode_jpadmin",
                password="Soulkidd0809@",
                database ="jodomode_example.db",
                port=3306)
            
            print("Conexxion exitosa a MariaDB")
            return conexion
        except mariadb.Error as e:
            print(f"Error conectando a MariaDB: {e}")
            sys.exit(1)

conn = conectar()
cursor = conn.cursor()
cursor.execute('SELECT VERSION()')
version = cursor.fetchone()
print(f"Version de mariaDB: {version[0]}")
cursor.close()
conn.close()
