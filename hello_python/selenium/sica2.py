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

#Selecciona el input y escribe el codigo del cliente
input_codigo = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".form-control.todo-list-input.input-event")))
input_codigo.send_keys("123456")

#Selecciona el boton buscar
boton_buscar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".add.btn.btn-primary.todo-list-add-btn")))
boton_buscar.click()

#Selecciona el cliente que salio en caso de que haya encontrado uno
resultado = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".d-flex.align-items-center.py-1.border-bottom.mt-1")
))
resultado.click()

time.sleep(1.5)

#----------- INPUT CEDULA -----------
xpath_cedula = '//input[@title="Cédula"]'
elemento_cedula = driver.find_element(By.XPATH, xpath_cedula)
elemento_cedula.send_keys("v7249487")

time.sleep(1)

BUTTON_XPATH = '//input[@title="Cédula"]/following::button[text()="Buscar"][1]'
espera_maxima = 10 # 10 segundos

try:
    # 2. Inicializar la espera
    wait = WebDriverWait(driver, espera_maxima)

    # 3. Esperar a que el elemento sea Clickeable
    # La condición EC.element_to_be_clickable() espera que el elemento esté presente, visible
    # Y lo más importante, habilitado (no deshabilitado).
    elemento_boton = wait.until(
        EC.element_to_be_clickable((By.XPATH, BUTTON_XPATH))
    )

    # 4. Interactuar con el elemento
    elemento_boton.click()
    print("✅ Clic realizado en el botón 'Buscar'.")

except TimeoutError:
    print(f"❌ Error: El botón 'Buscar' no se volvió clickeable después de {espera_maxima} segundos.")
except Exception as e:
    print(f"❌ Ocurrió un error al intentar hacer clic: {e}")
    
boton_buscar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".add.btn.btn-primary.todo-list-add-btn")))
    

PATH_CONDUCTOR = "(//div[@class='d-flex align-items-center py-1 border-bottom mt-1'])[1]"

try:
  wait = WebDriverWait(driver, espera_maxima)
  elemento_conductor = wait.until(EC.visibility_of_element_located((By.XPATH, PATH_CONDUCTOR)))
  elemento_conductor.click()
  print("✅ Resultado de conductor seleccionado con éxito.")
  
except TimeoutError:
  print(f"❌ Error: El elemento resultado de la búsqueda no apareció después de {espera_maxima} segundos")
except Exception as e:
  f"❌ Ocurrió un error al intentar hacer clic en el elemento: {e}"


#----------- INPUT VEHICULO -----------

XPATH_VEHICULO = '//input[@title="Placa"]'
input_vehiculo = driver.find_element(By.XPATH, XPATH_VEHICULO)
input_vehiculo.send_keys("a68aj4d")


BUSCAR_VEHICULO_PATH ='//input[@title="Placa"]/following::button[text()="Buscar"][1]'
boton_buscar_vehiculo = wait.until(EC.element_to_be_clickable((By.XPATH, BUSCAR_VEHICULO_PATH)))
boton_buscar_vehiculo.click()

RESULTADO_VEHICULO_PATH = "(//div[@class='d-flex align-items-center py-1 border-bottom mt-1'])[1]"
seleccionar_vehiculo = wait.until(EC.visibility_of_element_located((By.XPATH, RESULTADO_VEHICULO_PATH)))
seleccionar_vehiculo.click()

#----------- SELECCION DE PRODUCTO -----------

# Usamos la clase más distintiva y estable del contenedor
SPAN_SELECTOR = 'span.select2-selection.select2-selection--single'
espera_maxima = 10 

try:
    wait = WebDriverWait(driver, espera_maxima)

    # Esperar a que el span sea clickeable
    span_element = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, SPAN_SELECTOR))
    )

    # Hacer clic para ABRIR el desplegable
    span_element.click()
    print("✅ Clic realizado en el span Select2. Lista desplegable abierta.")

except Exception as e:
    print(f"❌ Error al intentar abrir el desplegable Select2: {e}")

# Reemplaza 'OPCION_DESEADA' con el texto visible que necesitas
OPCION_TEXTO = "PASTAS ALIMENTICIAS LEY ORGANICA DE PRECIO JUSTO" 

# XPath genérico para Select2: busca un <li> con la clase de resultado y el texto.
OPCION_XPATH = f'//li[contains(@class, "select2-results__option") and text()="{OPCION_TEXTO}"]'

try:
    # Esperar a que la opción aparezca y sea clickeable
    opcion_element = wait.until(
        EC.element_to_be_clickable((By.XPATH, OPCION_XPATH))
    )

    # Hacer clic en la opción para seleccionarla y cerrar el desplegable
    opcion_element.click()
    print(f"✅ Opción '{OPCION_TEXTO}' seleccionada con éxito.")

except Exception as e:
    print(f"❌ Error al intentar seleccionar la opción '{OPCION_TEXTO}': {e}")




#link del area de despacho https://sica.sunagro.gob.ve/despachos
#link del area de registro de despacho https://sica.sunagro.gob.ve/despachos/registrar

option = input('Ingrese una opcion: ')

match option:
  case 1:
    driver.get("https://sica.sunagro.gob.ve/despachos/registrar")




# Mostrar el título de la página para confirmar que se cargó
print("Título de la página:", driver.title)

input("PResiona enter para cerrar")

# Esperar unos segundos antes de cerrar (opcional)
# driver.implicitly_wait(5)


# Cerrar el navegador
driver.quit()