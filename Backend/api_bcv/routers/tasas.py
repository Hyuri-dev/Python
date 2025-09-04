from fastapi import APIRouter , HTTPException
from pydantic import BaseModel
import obtener_tasa
from datetime import datetime

class TasaResponse (BaseModel):
  """
  Modelo para la tasa cambiaria
  """
  fecha: str
  valor: float

router = APIRouter(prefix="/tipos-de-tasas", tags=["Tasas"], responses={404: {"Message": "Not Found/No encontrado"}})

@router.get("/usdbcv", response_model=TasaResponse)
async def obtener_bcv():
  fecha = datetime.now() #Obtenemos la fecha del dia
  fecha_formateada = fecha.strftime('%d-%m-%y') #Formateamos la fecha a formato d/m/y
  
  try:
    tasa_valor = obtener_tasa.obtener_bcv() #Obtenemos la tasa con la funcion del archivo obtener tasa
    return {"fecha": fecha_formateada , "valor": tasa_valor} # Retornamos el valor de la tasa del dia de hoy
  except ValueError as e:
    raise HTTPException(status_code= 404, detail=str(e))
  

