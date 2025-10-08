import requests
import time

URL = "http://localhost:8000"

def print_test (name):
    print(f"⁄n 🧩 {name} ⁄n" + "-" * 50)

print_test("Prueba 1: Login Correcto (admin) y acceso a /admin/")
resp = requests.post(f"{URL}/token", data={"username": "admin", "password": "aquiles"})
if resp.status_code == 200:
    token = resp.json()["access_token"]
    print(token)
    headers= {"Authorization": f"Bearer {token}"}
    admin_resp = requests.get(f"{URL}/admin/", headers=headers)
    print("Status:", admin_resp.status_code)
    print("Respuesta:", admin_resp.json())
else:
    print("Error al obtener el token:", resp.text)


# 2. Prueba si el usuario no existe
print_test("Prueba 2: Login con usuario equvocado o no existe")
resp =  requests.post(f"{URL}/token", data={"username": "aqui", "password": "abc"})
print("Status: ", resp.status_code)
print("Respuesta", resp.json())

# 3. Prueba si la contraseña es incorrecta
print_test("Prueba 3: Login con contraseña equivocada ")
resp =  requests.post(f"{URL}/token", data={"username": "admin", "password": "123"})
print("Status: ", resp.status_code)
print("Respuesta", resp.json())

#4. Prueba acceso a /admin/ sin token
print_test("Prueba 4: Acceso a /admin/ sin token")
resp =  requests.get(f"{URL}/admin/")
print("Status: ", resp.status_code)
print("Respuesta", resp.json())

#5. Prueba acceso a admin con usuario normal

print_test("Prueba 5: Login con usuario normal y acceso a /admin/")
resp = requests.post(f"{URL}/token", data={"username": "mandarino", "password": "mandarino2206"})
if resp.status_code == 200:
    token = resp.json()["access_token"]
    print(token)
    headers= {"Authorization": f"Bearer {token}"}
    admin_resp = requests.get(f"{URL}/admin/", headers=headers)
    print("Status:", admin_resp.status_code)
    print("Respuesta:", admin_resp.json())
else:
    print("Error al obtener el token:", resp.text)

#6. Acceso con token falso o corrupto
print_test("Prueba 6: Acceso con token falso o corrupto")
headers= {"Authorization": "Bearer eyJ.invalid.token"}
resp= requests.get(f"{URL}/admin/", headers=headers)
print("Status: ", resp.status_code)
print("Respuesta", resp.json())