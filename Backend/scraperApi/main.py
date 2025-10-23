from  fastapi import FastAPI
from pydantic import BaseModel

class Product(BaseModel):
  url: str



app = FastAPI()

@app.get("/")
async def init ():
  return {"Message: Api Scrapper is running, read the doc for more info."}

@app.post("/search")
async def search ():
  pass