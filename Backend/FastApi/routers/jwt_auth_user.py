from fastapi import APIRouter, Depends, HTTPException,status, FastAPI
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime , timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1

crypt = CryptContext(schemes=["bcrypt"])

app = FastAPI()

# router = APIRouter(prefix="/jwtauth", tags=["jwtauth"], responses={status.HTTP_404_NOT_FOUND: {"Message": "No encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email:str
    disabled: bool

class Userdb (User):
    password: str

users_db = {
    "Hyuri": {
        "username": "hyuri",
        "full_name": "Hyuri.dev",
        "email": "Hyuri.dev@developer.com",
        "disabled": False,
        "password": "$2a$12$CQOUjvBCyWWRk48p/BPHHOhXIk7IPaD4HkBjohc0ljcSUceMs2lzS",
    },
        "Hyuri2": {
        "username": "hyuri2",
        "full_name": "Hyuri2.dev",
        "email": "Hyuri2.dev@developer.com",
        "disabled": True,
        "password": "$2a$12$SD0tHm7xXgO6oxF4qmN6eepTy9bdNooWGmEOVjA.Lmzo5Z8DREPme", #Hemos encripatado las contraseñas con un encriptador onlines bcryp generator   
    }
}

def search_user(username: str):
    if username in users_db:
        return users_db(users_db[username])

@app.post("/login-jwt")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    
    if not user_db:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="El Usuario no es correcto")
    
    user = search_user(form.username)
    
    if not crypt.verify(form.password, user.password): #Verify nos verifica si la contraseña ingresada en el formulario es la misma que la de la base de datos
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    # access_token_expiration =  timedelta(minutes=ACCESS_TOKEN_DURATION) # Hay que calcular cuanto tiempo va a durar el token, para esto utilizamos la libreria time e importamos delta
    access_token = {"sub": user.username, "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    }
    
    return {"access_token": access_token , "token_type": "bearer"}