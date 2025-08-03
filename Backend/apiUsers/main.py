from fastapi import FastAPI
from routers import users


#Creamos una instancia del objeto fastapi
app = FastAPI()

# Endpoint base para el API, Es donde principalmente irian y corroborar que esta en funcionamiento
@app.get("/inicio")
async def hola ():
    return {"Bienevenido al API de usuarios de hyuri.dev"}

app.include_router(users.router)

