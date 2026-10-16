from playwright.async_api import async_playwright, expect
# import pywhatkit as ws
from datetime import date
import sys 
import os
from pathlib import Path
import asyncio



async def obtener_bcv():
    """Obtiene la tasa del BCV y guarda una captura."""
    BASE_DIR = Path(__file__).resolve().parent.parent
    OUTPUT_DIR = BASE_DIR / "assets"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ruta_screenshot = OUTPUT_DIR / "TASA.png"

    async with async_playwright() as p:
        # Creamos un navegador headless y un contexto para simular un usuario.
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        await page.goto("https://www.bcv.org.ve/")

        localizador = page.locator(
            ".views-row.views-row-1.views-row-odd.views-row-first.views-row-last.row"
        )
        await localizador.screenshot(path=str(ruta_screenshot))
        localizador_tasa = page.locator("#dolar .col-sm-6.col-xs-6.centrado strong")
        tasa_usd = await localizador_tasa.last.inner_text()
        tasa_formateada  = tasa_usd.replace(",", ".")
        tasa_convertida = float(tasa_formateada)
        print(f"La tasa es: {round(tasa_convertida, 4)} y se ha guardado una captura.")
        await browser.close()
        return tasa_convertida
    
    
    
    #---------> Enviar el mensaje por ws <---------
    
#     DATE = date.today() 
#     formated_date = DATE.strftime("%d/%m/%Y")
#     number = "+584126350266"
#     image = resource_path(r"C:\Users\Personal\python\Python\Projects\scriptTasaBcv\assets\tasas.png")
#     caption = f"""TASA DEL DIA {formated_date} ES DE: {tasa_convertida}
# - Agradecemos utilizar los 4 dígitos para mas precisión en los montos. 
# - Verifiquen que los pagos sean correspondientes a la tasa del día y al monto de la factura, en caso de que el pago sea menor identificar el monto del abono. 
# - Por favor al recibir los pagos notifíquelo a la brevedad posible en el grupo de cobranza para mantener las cuentas lo mas al día y real posible. 
# - Evite enviar pagos duplicados, siempre verifiquen la información antes de enviarlo"""
    
#     ws.sendwhats_image(number, img_path= image, caption=caption, tab_close=True)
    
#     print("Mensaje enviado con exito !")
#     browser.close()



if __name__ == "__main__":
  obtener_bcv()