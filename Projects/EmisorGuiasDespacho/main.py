import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        
        browser = await p.chromium.launch(headless=False, channel="chrome")
        page = await browser.new_page()
        
        print("Intentando navegar a SUNAGRO...")
        await page.goto("https://sica.sunagro.gob.ve/login")
        
        print(f"Página actual: {page.url}")
        print(f"Título de la página: {await page.title()}")
        
        await page.get_by_label("Close").click()
        
        await page.locator("#exampleInputEmail").fill("gruponovoeu")
        await page.locator("#passwordInput").fill("lasublime1988")
        
        await page.get_by_role("button", name="Continuar").click()
        
        
        await page.goto("https://sica.sunagro.gob.ve/despachos/registrar")
        
        await page.get_by_placeholder("FACTURA(S)").fill("123")
        
        await page.get_by_title("Código").fill("5459")
        
        await page.get_by_role("button", name="Buscar").click()
        
        
        
        input("Prueba exitosa. Presiona Enter para cerrar.")
        await browser.close()

asyncio.run(main())