from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import os
from dotenv import load_dotenv

load_dotenv()

driver = webdriver.Chrome()
driver.get("https://sica.sunagro.gob.ve/login")

wait = WebDriverWait(driver, 10)

usuario = wait.until(EC.visibility_of_element_located((By.ID, "exampleInputEmail")))
password = wait.until(EC.visibility_of_element_located((By.ID, "passwordInput")))

cerrar_modal = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "close")))

#Cerramos el modal
cerrar_modal.click()

usuario.send_keys(os.getenv('USER'))
password.send_keys(os.getenv('PASSWORD'))

time.sleep(3)

# Botón de login
login_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "auth-form-btn")))
login_btn.click()

codigo_elemento = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".card-text.my-2")))
texto = codigo_elemento.text

codigo = re.search(r"CÓDIGO PARA CONTINUAR\. (\d+)", texto)

if codigo:
  codigo_acceso = codigo.group(1)
  input_codigo = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "form-control")))
  input_codigo.send_keys(codigo_acceso)
else:
  print("No se encontro el codigo en el texto.")

opcion = int(input("Seleccione una opcion: "))

if opcion == 1:
  wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".bt.btn-primary"))).click()
elif opcion == 2:
  wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "CERRAR SESIÓN"  ))).click()
  

input("Presiona enter para cerrar la prueba")
driver.quit()