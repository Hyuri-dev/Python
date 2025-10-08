from selenium import webdriver
from selenium.webdriver.common.by import By

#Creamos un driver

driver = webdriver.Chrome()

#Hacemos unaa accion, en esta ocasion navegamos a un sitio

driver.get("https://www.selenium.dev/selenium/web/web-form.html")

#Solicitamos información al navegador

title = driver.title

#Establecemos ahora una espera, ya que no podemos buscar elementos si no estan renderizados en la pagina

driver.implicitly_wait(5)

# Buscamos un elemento
text_box = driver.find_element(by=By.NAME, value="my-text")
submit_button = driver.find_element(by=By.CSS_SELECTOR , value="button")

#Hacer una accion con los elementos

text_box.send_keys("Selenium")
submit_button.click()

#Solicitamos nuevamente la informació del elemento

message = driver.find_element(by=By.ID, value="message")
text = message.text

print(text)

#Quitamos el driver
driver.quit()