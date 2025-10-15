from playwright.sync_api import sync_playwright, expect


def test_obtener_tasa():
  with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    page.goto("https://hello-javascript-kappa.vercel.app/index.html")
    localizador = page.locator("#tasa_actual span")
    texto = localizador.screenshot(path="tasa.png")
    
    print(texto)
    browser.close()


def obtener_bcv():
  with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    page.goto("https://www.bcv.org.ve/")
    
    localizador = page.locator(".views-row.views-row-1.views-row-odd.views-row-first.views-row-last.row")
    resultado = localizador.screenshot(path="C:\\Users\\Personal\\python\\Python\\hello_python\\scraping\\assets\\tasas.png")
    print(resultado)
    browser.close()

if __name__ == "__main__":
  # test_obtener_tasa()
  obtener_bcv()