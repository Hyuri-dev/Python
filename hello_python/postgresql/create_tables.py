import psycopg2

def create_tables():
    """Create tables in postgresql db
    """
    commands =(
    """
    CREATE TABLE IF NOT EXISTS mensajes (
        mensaje_id SERIAL PRIMARY KEY,
        mensaje_contenido VARCHAR(255) NOT NULL
    );
    """
    )
    try:
        conn = psycopg2.connect("postgresql://example_1ula_user:TS3mlURmO9E3FAnIUWjSugX4nWqwfVKc@dpg-d2tfclnfte5s73a6kbq0-a.oregon-postgres.render.com/example_1ula")
        cur = conn.cursor()
        cur.execute(commands)
        conn.commit()
        cur.close()
        conn.close()
        print("Tabla 'mensajes' creada exitosamente!")
    except(psycopg2.DatabaseError, Exception) as error:
        print("eroror al crear la tabla",error)


if __name__ == '__main__':
    create_tables()