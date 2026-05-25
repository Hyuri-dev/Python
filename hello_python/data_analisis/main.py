import os
from dotenv import load_dotenv

load_dotenv()

RUTA = os.getenv("JULIO")

print(os.getenv("JULIO"))

print(f"Encontrada la ruta de julio: {RUTA}")