import requests

URL = "https://fast-api-msg-example.onrender.com/"

def crear_mensaje():
  mensaje = input("Ingrese el mensaje: ")
  datos = {
    "text": f"{mensaje}"
  }
  resp = requests.post(f"{URL}/messages", json= datos)
  
  if resp.status_code == 201:
    print('Mensaje enviado con exito.')
    print('Respuesta del servidor: ', resp.json())
  else:
    print(f"Error al enviar el mensaje. Codigo de estado: {resp.status_code}")
    print('Detalles del error:', resp.text)

crear_mensaje()