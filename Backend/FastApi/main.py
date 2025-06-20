from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root ():
    return "Hola FastApi!2"


@app.get("/url") #Para poder añadir otro get hace falta poder añadir una nueva ruta al path, ya que el / solo es el path main o raiz
async def root ():
    return {"url": "google.com", "url2": "youtube.com"} # El formato por defecto para crear api es escribir en diccionario clave valor, mas especifico en formato json es el standar con el que se trabaja #