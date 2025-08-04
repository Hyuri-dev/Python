from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import session
import crud , models, schemas
from database import SessionLocal, engine
from routers import users

models.Base.metadata.create_all(bind= engine)
#Creamos una instancia del objeto fastapi
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint base para el API, Es donde principalmente irian y corroborar que esta en funcionamiento
@app.get("/inicio")
async def hola ():
    return {"Bienevenido al API de usuarios de hyuri.dev"}


#Endpoint para crear usuarios con la base de datos
@app.post("/user/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: session = Depends(get_db)): #verificamos si el usuario tiene el email y el password
    db_user= crud.get_email(db, email= user.email) #revisamos si ya existe
    if db_user:
        raise HTTPException(status_code= 400, detail= "Email already registered") #Si existe mandamos un mensaje de error
    return crud.create_user(db=db, user=user) # Si no existe entonces crea el usuario

@app.get("/user", response_model=list[schemas.User])
def read_users(skip: int = 0, limit : int = 100, db:session = Depends(get_db)):
    users = crud.get_users(db, skip = skip , limit = limit)
    return users


@app.get("/user({user_id})", response_model=schemas.User)
def read_users(user_id: int, db:session = Depends(get_db)):
    db_user= crud.get_user(db, user_id = user_id)
    if db_user is None:
        raise HTTPException(status_code= 404, detail= "User not found")
    return db_user











app.include_router(users.router)

