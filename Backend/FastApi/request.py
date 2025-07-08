import requests

URL = "http://127.0.0.1:8000/url"

respuesta = requests.get(URL)

data = respuesta.json()
print("Solicitud creada con exito")
print(f'URL: {data}')