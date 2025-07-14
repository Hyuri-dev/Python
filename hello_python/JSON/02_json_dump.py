import json as js

vendedor = {
  "id": "01",
  "nombre": "victor",
  "activo": False
}

#Si queremos crear un diccionario de python a json utilzamos la funcion dumps

vendedor_JSON = js.dumps(vendedor, indent=2, sort_keys=True) # el parametro indent nos indenta el contenido del json., sort ordena las clave en orden alfabetico
print(vendedor_JSON)
print(vendedor)

