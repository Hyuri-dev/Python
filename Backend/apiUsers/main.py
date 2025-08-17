from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
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
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)): #verificamos si el usuario tiene el email y el password
    db_user= crud.get_email(db, email= user.email) #revisamos si ya existe
    if db_user:
        raise HTTPException(status_code= 400, detail= "Email already registered") #Si existe mandamos un mensaje de error
    return crud.create_user(db=db, user=user) # Si no existe entonces crea el usuario

#Endpoint para obtener usuarios desde la bd
@app.get("/list-user", response_model=list[schemas.User])
def read_users(skip: int = 0, limit : int = 100, db:Session = Depends(get_db)):
    users = crud.get_users(db, skip = skip , limit = limit)
    return users

#Obtener un usuario en base de su id 
@app.get("/user({user_id})", response_model=schemas.User)
def read_users(user_id: int, db:Session = Depends(get_db)):
    db_user= crud.get_user(db, user_id = user_id)
    if db_user is None:
        raise HTTPException(status_code= 404, detail= "User not found")
    return db_user

# Crear un item para un usuario 
@app.post("/user/{user_id}/create-items/", response_model=schemas.Item)
def create_item_for_user (user_id : int , item : schemas.ItemCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code= 4040, detail= "User not found")
    return crud.create_user_item(db=db, item=item, user_id=user_id)


# borrar usuario
@app.delete("/user/{user_id}")
def  delete_user ( user_id: int , db: Session = Depends(get_db)):
    success = crud.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code= 404, detail="User not found")
    return{"detail": "User deleted succesfully"}


@app.get("/get-items", response_model=list[schemas.Item])
def read_items(skip:int = 0 , limit: int = 100, db: Session = Depends (get_db)):
    items = crud.get_items(db, skip=skip ,limit=limit)
    return items

@app.put("/items/{item_id}", response_model= schemas.Item)
def update_items(item_id : int , item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = crud.update_item(db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail= "Item not found")
    return db_item

@app.delete("/items/{item_id}")
def  delete_item ( item_id: int , db: Session = Depends(get_db)):
    success = crud.delete_item(db, item_id=item_id)
    if not success:
        raise HTTPException(status_code= 404, detail="Item not found")
    return{"detail": "Item deleted succesfully"}











# app.include_router(users.router)