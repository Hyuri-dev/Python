import os
from supabase import create_client , Client
from dotenv import load_dotenv

load_dotenv()
url: str = os.environ.get("URL")
key: str = os.environ.get("KEY")

supabase: Client = create_client(url,key)

response = (supabase.table("usuarios").insert({"nombre_usuario": "admin"})
            )

def insertar():
  nombre = "admin"
  supabase.table("usuarios").insert({"id":2,"nombre_usuario": f"{nombre}"})
  print(f"Creado el usuario: {nombre}")

insertar()
listar = (supabase.table("usuarios").select("*").execute()
            )

print(f"Usuarios: {listar}")
