from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Configuración básica del navegador
chrome_options = Options()
# Puedes comentar estas líneas si no necesitas usar un perfil específico
chrome_options.add_argument("--user-data-dir=C:/Users/personal/AppData/Local/Google/Chrome/User Data")
chrome_options.add_argument('--profile-directory=Profile 4')

# Inicializar el navegador
driver = webdriver.Chrome(options=chrome_options)

# Abrir la página
driver.get("https://sica.sunagro.gob.ve/login")

# Mostrar el título de la página para confirmar que se cargó
print("Título de la página:", driver.title)

# Esperar unos segundos antes de cerrar (opcional)
driver.implicitly_wait(5)

# Cerrar el navegador
driver.quit()