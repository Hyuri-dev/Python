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
        
        # Codigo del cliente
        inputCodSica = page.get_by_title("Código")
        await inputCodSica.fill("974949")
        
        buscarCodigo = inputCodSica.locator('..').get_by_role("button", name="Buscar")
        await buscarCodigo.click()
        selectorResultado = "div.d-flex.align-items-center.border-bottom"
        await page.locator(selectorResultado).nth(0).click()
        
        #Cedula chofer
        inputCedula = page.get_by_title("Cédula")
        await inputCedula.fill("v7184360")
        
        buscarCedula = inputCedula.locator("..").get_by_role("button", name="Buscar")
        await buscarCedula.click()
        await page.locator(selectorResultado).nth(1).click()

        
        #Placa camion
        inputPlaca = page.get_by_title("Placa")
        await inputPlaca.fill("A28AS9G")
        
        buscarPlaca = inputPlaca.locator("..").get_by_role("button", name="Buscar")
        await buscarPlaca.click()
        await page.locator(selectorResultado).nth(2).click()
        
        #Producto
        producto = "PASTAS ALIMENTICIAS LEY ORGANICA DE PRECIO JUSTO"
        
        await page.get_by_role("combobox").click()
        
        
        campoBusqueda = page.locator(".select2-search__field")
        await campoBusqueda.wait_for()
        await campoBusqueda.type(text=producto, delay=50)
        
        resultado = page.get_by_role("treeitem", name=producto)
        await resultado.wait_for()
        await resultado.click()
        
        input("Prueba exitosa. Presiona Enter para cerrar.")
        await browser.close()

asyncio.run(main())