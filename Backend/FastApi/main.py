from fastapi import FastAPI
from routers import products , users, basic_auth_user, jwt_auth_user
from fastapi.staticfiles import StaticFiles

app = FastAPI()


@app.get("/")
async def root ():
    return "Hola FastApi!2"

#Routers
#los routers nos permiten enrutar otros modulos de nuestra api para asi conectarlas en total y correrlo todo en un solo servidor con un archivo pero que contiene el enrutado de los demas api's
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_user.router)
app.include_router(jwt_auth_user.router)
app.mount("/static", StaticFiles(directory="statics"), name="static")  #Mount nos declara el path donde va a estar esos recursos y su nombre por donde se ira a buscar en el api
#si necesitaramos montar archivos estaticos en nuestro api, podria ser un pdf, una imagen, etc
# Aplicariamos el mount desde el app y tambien a su vez llamariamos a importar con fastapi el atributo staticfiles#



@app.get("/url") #Para poder añadir otro get hace falta poder añadir una nueva ruta al path, ya que el / solo es el path main o raiz
async def url ():
    return {"url": "google.com", "url2": "youtube.com"} # El formato por defecto para crear api es escribir en diccionario clave valor, mas especifico en formato json es el standar con el que se trabaja #

#La propia api tiene una documentacion predeterminada hecha con swagger  a la cual podemos acceder con 
# http://127.0.0.1:8000/docs

#Para iniciar el servidor de uvicorn ejecutamos fastapi dev <nombre de tu archivo>
# Pära detener el servidor presionamos ctrl + c