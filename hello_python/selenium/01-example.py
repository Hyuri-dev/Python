from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv

driver = webdriver.Chrome()
driver.get("https://www.amazon.com")

# Localizar la barra de búsqueda
search_box = driver.find_element(By.ID, "twotabsearchtextbox")
search_box.send_keys("laptop")
search_box.send_keys(Keys.RETURN)

# Esperar a que carguen los resultados
time.sleep(3)

# Localizar los elementos de los resultados
# Nota: Los selectores de Amazon pueden cambiar, así que puede que necesites ajustarlos.
results = driver.find_elements(By.CSS_SELECTOR, "div[data-component-type='s-search-result']")

products = []

for result in results[:10]:  # Solo los primeros 10
    try:
        title = result.find_element(By.CSS_SELECTOR, "h2 a span").text
        price = result.find_element(By.CSS_SELECTOR, ".a-price-whole").text
        products.append([title, price])
    except:
        # Si no encuentra el precio, lo omitimos
        continue

# Guardar en CSV
with open('productos.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Título", "Precio"])
    writer.writerows(products)

driver.quit()