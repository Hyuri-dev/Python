from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field, EmailStr, field_validator
import re

router = APIRouter(prefix="/user", tags=["user"], responses={404: {"Message": "No Encontrado"}})
# El prefijo es lo que se llama primero y luego se llama el endpoint a acceder es decir: localhost:80000/user/users
class User (BaseModel):
    id: int
    username: str = Field(...,min_length=3, max_length=20)
    email: EmailStr
    password: int 

listado_usuarios = [
    User(id= 1, username="Hyuri", email="hyuri@hotmail.com", password=123456)
]

@router.get("/users/") #Obtiene el listado de usuarios
async def get_users():
    return listado_usuarios

@router.post("/")
async def create_users (usuario: User):
    listado_usuarios.append(usuario)
    return usuario


@router.delete("/deleteuser/{id}")
async def delete_user (id: int):
    found = False
    
    for index , saved_user in enumerate(listado_usuarios):
        if saved_user.id == id:
            del listado_usuarios[index]
            found = True
            return {"Message": "Eliminacion exitosa"}
        if not found:
            return {"Error": "No se ha elimidando el usuario"}

@router.put("/user/{id}")
async def update_user (id: int, user: User = Body(
    ..., example= {
        "id": "00",
        "username": "ExampleUser",
        "email": "Example@",
        "password": "1111"
        }),): return {"id": id, "usuario": user}