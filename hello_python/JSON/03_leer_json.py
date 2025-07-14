import json as js
import os

archivo = os.path.join("hello_python\\JSON\\ordenes.json")

with open(archivo) as archivo:
    datos = js.load(archivo)

print(len(datos["ordenes"]))

print(datos["ordenes"][0]["delivery"])
#Si quisieramos acceder a un valor de una de las ordenes del json que tenemos tendriamos que llamar a la clave principal es decir a ordenes, el indice de la orden a la que queremos acceder que en este caso seria el primero es decir, 0 ,  y por ultimo la clave que queremos consultar, en este caso delivery



