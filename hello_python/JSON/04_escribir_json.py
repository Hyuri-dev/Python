import json
import os

ruta = os.path.join("hello_python\\JSON\\ordenes.json")

#Para escribir, reescribir un json utilizamos una sentencia similar a cuando queremos leer un json
with open (ruta) as archivo:
  datos = json.load(archivo)
  print("Datos cargados correctamente")
    #Crearemos un for para eliminar el cliente de los pedidos contenidos en el json y asi crear un nuevo archivo posteriormente
  for orden in datos ["ordenes"]:
      del orden["cliente"] # borramos de la clave principal ordenes la clave cliente




#Creamos un nuevo archivo
#Para guardar los cambios

with open ("ordenes_nuevas.json", "w") as archivo_nuevo:
  json.dump(datos, archivo_nuevo)

print(archivo)
print(archivo_nuevo)

