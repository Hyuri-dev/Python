import json as js

vendedor = {
  "id": "01",
  "nombre": "victor",
  "activo": False
}

#Si queremos crear un diccionario de python a json utilzamos la funcion dumps

vendedor_JSON = js.dumps(vendedor, indent=2) # el parametro indent nos indenta el contenido del json.

print(vendedor_JSON)
print(vendedor)