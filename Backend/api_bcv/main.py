from fastapi import FastAPI
from routers import tasas




app = FastAPI()

app.include_router(router=tasas.router)

@app.get("/inicio")
async def root():
  return {"Bienvenidos al api para consulta del BCV, te recomiendo ingresar a la documentacion para visualizar mejor como funcionan los endpoints :)"}
