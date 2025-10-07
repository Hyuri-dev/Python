from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración básica del navegador
chrome_options = Options()
# Puedes comentar estas líneas si no necesitas usar un perfil específico
chrome_options.add_argument("--user-data-dir=C:/Users/personal/AppData/Local/Google/Chrome/User Data")
chrome_options.add_argument('--profile-directory=Profile 1')

# Inicializar el navegador
driver = webdriver.Chrome(options=chrome_options)


# Abrir la página
driver.get("https://sica.sunagro.gob.ve/login")

wait = WebDriverWait(driver, 10)

usuario = wait.until(EC.visibility_of_element_located((By.ID, "exampleInputEmail")))
password = wait.until(EC.visibility_of_element_located((By.ID, "passwordInput")))

cerrar_modal = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "close")))

#Cerramos el modal
cerrar_modal.click()

usuario.send_keys(os.getenv('USER2'))
password.send_keys(os.getenv('PASSWORD1'))

time.sleep(1.5)

# Botón de login
login_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "auth-form-btn")))
login_btn.click()

time.sleep(1.5)


driver.get("https://sica.sunagro.gob.ve/despachos/registrar")

time.sleep(1.5)

# Selecciona el textarea por ambas clases
textarea = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".form-control.input-event")))
textarea.send_keys("1564")

time.sleep(1.5)

input_codigo = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".form-control.todo-list-input.input-event")))
input_codigo.send_keys("123456")

boton_buscar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".add.btn.btn-primary.todo-list-add-btn")))
boton_buscar.click()

resultado = wait.until(EC.visibility_of_element_located(
    (By.CSS_SELECTOR, ".d-flex.align-items-center.py-1.border-bottom.mt-1")
))
resultado.click()





#link del area de despacho https://sica.sunagro.gob.ve/despachos
#link del area de registro de despacho https://sica.sunagro.gob.ve/despachos/registrar


# Mostrar el título de la página para confirmar que se cargó
print("Título de la página:", driver.title)

input("PResiona enter para cerrar")

# Esperar unos segundos antes de cerrar (opcional)
# driver.implicitly_wait(5)


# Cerrar el navegador
driver.quit()