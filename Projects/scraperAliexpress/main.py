from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

url = "https://n9.cl/sd778"
SELECTOR_TITULO = 'h1[data-pl="product-title"]'
SELECTOR_PRECIO = 'span[class^="price-default--current--"]'

# --- Configuración (Basada en tu URL y selectores) ---
URL_BASE_COMPLETA = "https://es.aliexpress.com/item/32832114082.html?spm=a2g0o.productlist.main.1.5abb41a47YwWtO&algo_pvid=9872b754-af5e-408c-be7d-93985fd9ac6f&algo_exp_id=9872b754-af5e-408c-be7d-93985fd9ac6f-0&pdp_ext_f=%7B%22order%22%3A%228%22%2C%22eval%22%3A%221%22%7D&pdp_npi=6%40dis%21USD%214.24%213.60%21%21%214.24%213.60%21%402101c59117559981707892287e0ca2%2165107196330%21sea%21VE%210%21ABX%211%210%21n_tag%3A-29910%3Bd%3Ad3f6874%3Bm03_new_user%3A-29895&curPageLogUid=FqBHxtUhWn5a&utparam-url=scene%3Asearch%7Cquery_from%3A%7Cx_object_id%3A32832114082%7C_p_origin_prod%3A"

# Limpiamos la URL base quitando todos los parámetros de seguimiento.
URL_BASE_LIMPIA = URL_BASE_COMPLETA.split('?')[0] 

# 💰 URL FINAL FORZADA A USD. Esto es lo más importante.
URL_USD = f"{URL_BASE_LIMPIA}?currency=USD&country=US" 

SELECTOR_TITULO = 'h1[data-pl="product-title"]'
SELECTOR_PRECIO = 'span[class^="price-default--current--"]'


def scraper_aliexpress (url):
  with sync_playwright () as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context( user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36')
    page = context.new_page()

    print(f"abriendo {url}")

    page.goto(url, timeout=60000)

    try:
      page.wait_for_selector("h1")
      print("Elemento encontrado!")
    except Exception as e:
      print(f"Error no se encontro el selector clave ('{SELECTOR_TITULO}') despues de 10s")
      browser.close()
      return{"error": "No se pudo cargar o encontrar el contenido."}
    
    contenido_html = page.content()
    browser.close()

    soup = BeautifulSoup(contenido_html, 'html.parser')

    element_title = soup.select_one(SELECTOR_TITULO)
    titulo = element_title.text.strip() if element_title else "TITULO NO ENCONTRADO"

    element_price = soup.select_one(SELECTOR_PRECIO)
    precio = element_price.text.strip() if element_price else "PRECIO NO ENCONTRADO"
    print(f"El producto es: {titulo} y cuesta: {precio}")

    return {
      "URL": url,
      "Titulo":titulo,
      "Precio": precio
    }
  

if __name__ == "__main__":
    scraper_aliexpress(URL_USD)