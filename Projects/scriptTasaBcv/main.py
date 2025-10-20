from playwright.sync_api import sync_playwright, expect
import pywhatkit as ws
from datetime import date
import sys 
import os




def obtener_bcv():
  
  def resource_path (relative_path):
    """Obtener rula absoluta al recurso"""
    try:
      base_path = sys._MEIPASS
    except Exception:
      base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
  
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
    print(f'La tasa es: {round(tasa_convertida, 4)} y se ha guardado una captura.')
    
    
    
    #---------> Enviar el mensaje por ws <---------
    
    DATE = date.today() 
    formated_date = DATE.strftime("%d/%m/%Y")
    number = "+584126350266"
    image = resource_path(r"C:\Users\Personal\python\Python\Projects\scriptTasaBcv\assets\tasas.png")
    caption = f"""TASA DEL DIA {formated_date} ES DE: {tasa_convertida}
- Agradecemos utilizar los 4 dígitos para mas precisión en los montos. 
- Verifiquen que los pagos sean correspondientes a la tasa del día y al monto de la factura, en caso de que el pago sea menor identificar el monto del abono. 
- Por favor al recibir los pagos notifíquelo a la brevedad posible en el grupo de cobranza para mantener las cuentas lo mas al día y real posible. 
- Evite enviar pagos duplicados, siempre verifiquen la información antes de enviarlo"""
    
    ws.sendwhats_image(number, img_path= image, caption=caption, tab_close=True)
    
    print("Mensaje enviado con exito !")
    browser.close()



if __name__ == "__main__":
  obtener_bcv()