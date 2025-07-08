from fastapi import APIRouter, Depends, HTTPException,status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(prefix="/basicauth", tags=["basicauth"], responses={status.HTTP_404_NOT_FOUND: {"Message": "No encontrado"}})

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
        "password": "220601",
    },
        "Hyuri2": {
        "username": "hyuri2",
        "full_name": "Hyuri2.dev",
        "email": "Hyuri2.dev@developer.com",
        "disabled": True,
        "password": "soulkidd08",
    }
}

def search_user(username: str):
    if username in users_db:
        return users_db(users_db[username])

async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticacion invalidas", headers={"WWW-Authenticate": "Bearer"})
    return user

router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="El Usuario no es correcto")
    
    user = search_user(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    return {"access_token": user.username, "token_type": "bearer"}

router.get("users/me")
async def me(user: User = Depends(current_user)):
    return user
