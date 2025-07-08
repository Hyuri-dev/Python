import json as js
import os

archivo = os.path.join("hello_python\\JSON\\ordenes.json")

with open(archivo) as archivo:
    datos = js.load(archivo)

print(datos)