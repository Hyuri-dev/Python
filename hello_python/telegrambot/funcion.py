from playwright.sync_api import sync_playwright, expect




def obtener_bcv():
  with sync_playwright() as p:
    #Creamos un navegador, headless nos permite visualizar o no el navegador cuando arrancamos el script
    browser = p.chromium.launch(headless=True)
    #Creamos un contexto para el modo headless para asi simule la interaccion como un usuario
    context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")
    page = context.new_page()
    
    page.goto("https://www.bcv.org.ve/")
    
    localizador = page.locator(".views-row.views-row-1.views-row-odd.views-row-first.views-row-last.row")
    resultado = localizador.screenshot(path=r"C:\Users\Personal\python\Python\Projects\scriptTasaBcv\assets\tasas.png")
    localizador_tasa = page.locator(".col-sm-6.col-xs-6.centrado strong")
    tasa_usd = localizador_tasa.last.inner_text()
    tasa_formateada = tasa_usd.replace(',', ".")
    tasa_convertida = float(tasa_formateada)
    print(f'La tasa es: {round(tasa_convertida, 4)}')
    return tasa_convertida


if __name__ == "__main__":
  obtener_bcv()