from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

#Entidad usuario

class User(BaseModel):
    id: int
    name: str
    surname: str
    email:str
    age: int

user_list = [
    User(id= 1,name="Jefferson", surname="Stuwart" ,email= "Jeffry@gmail.com" , age= 23),
    User(id= 2,name="Areanna",surname= "Sofia",email= "Sofi@gmail.com", age= 22),
    User(id= 3,name="Carlos", surname="Arca",email= "minuriam@outlook.com", age= 33)
]


@app.get("/usersjson")
async def usersjson ():
    return  [{"name": "Jefferson" , "surname": "Stuwart", "email": "jeffry@gmail.com", "age": 23},
            {"name": "Mario" , "surname": "Malave", "email": "mariobro@gmail.com", "age": 45},
            {"name": "Areanna" , "surname": "Sofia", "email": "sofi@gmail.com", "age": 22} ]

@app.get("/users")
async def users ():
    return user_list

#Es posible buscar un valor en concreto asi que para ello es posible incluirle un valor al path
# aunque modificando tambien el nombre de la funcion para dejarlo lo mas claro posible y se entienda
# que hace esta nueva peticion o accion#

#Busqueda por path
@app.get("/user/{id}")
async def user (id:int):
    return search_user(id)

#Busqueda por query
@app.get("/userquery/")
async def user (id:int):
    return search_user(id)


def search_user(id: int):
    users = filter(lambda user: user.id == id, user_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado ningun usuario"}
