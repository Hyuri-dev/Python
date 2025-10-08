import psycopg2

def connect():
    """ Connect to the PostgreSQL database server """
    conn = psycopg2.connect(host="localhost", database="suppliers", user="postgres", password="aquiles")
    print(conn, "Conexion establecida!")

def connect_render():
    connection_url = "postgresql://example_1ula_user:TS3mlURmO9E3FAnIUWjSugX4nWqwfVKc@dpg-d2tfclnfte5s73a6kbq0-a.oregon-postgres.render.com/example_1ula"
    try:
        conn = psycopg2.connect(connection_url)
        print ("Conexion exitosa a render!")
        
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            db_version =cur.fetchone()
            print(f"version de la base de datos: {db_version}")
        conn.close()
    except psycopg2.Error as e:
        print(f"Error al conectar a la base de datos: {e}")

connect()

connect_render()
