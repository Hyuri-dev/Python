import json as js

#Para escribir un json de varias lineas utilizamos triple comillas
datos = """
{
  "tamaño": "mediana",
  "precio": 18.99,
  "toppings": ["champiñones","jamon","piña"],
  "cliente": {
    "nombre": "Jane Doe",
    "telefono": "0000000"
    
  }
}

"""
diccionario = js.loads(datos) #crea un diccionario con los pares clave-valor de la cadena de caracteres JSON y retorna este diccionario nuevo, asignando lo retornado a la variable en este caso

print(diccionario) # Comprobamos que se haya convertido el json en una lista
print(datos)

#Es posible acceder a los valores del json como si fuese un listado,  una vez convertido en una lista

print(diccionario["tamaño"])
print(diccionario["precio"])
print(diccionario["cliente"])
