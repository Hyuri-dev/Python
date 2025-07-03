from fastapi import APIRouter , HTTPException # htttpexception es una extension de fastapi para utilizar  status code en otras partes de nuestras solicitudes
from pydantic import BaseModel

router = APIRouter(prefix="/user" , tags=["user"], responses= {404: {"Message": "No encontrado"}})

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


@router.get("/usersjson")
async def usersjson ():
    return  [{"name": "Jefferson" , "surname": "Stuwart", "email": "jeffry@gmail.com", "age": 23},
            {"name": "Mario" , "surname": "Malave", "email": "mariobro@gmail.com", "age": 45},
            {"name": "Areanna" , "surname": "Sofia", "email": "sofi@gmail.com", "age": 22} ]

@router.get("/")
async def users ():
    return user_list

#Es posible buscar un valor en concreto asi que para ello es posible incluirle un valor al path
# aunque modificando tambien el nombre de la funcion para dejarlo lo mas claro posible y se entienda
# que hace esta nueva peticion o accion#

#Busqueda por path: su uso por lo general se emplea en busquedas de parametros fijos
@router.get("/{id}")
async def user (id:int):
    return search_user(id)

#Busqueda por query:  Su uso se emplea en busquedas de parametros que pueden estar o no estar
@router.get("/query")
async def user (id:int):
    return search_user(id)


def search_user(id: int):
    users = filter(lambda user: user.id == id, user_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado ningun usuario"}

# Operacion POST, si queremos crear una peticion al api para enviar datos, podemos hacerlo utilizando el metodo post
#Este metodo nos sirve para enviarle datos a nuestra API

@router.post("/", response_model= User ,status_code= 201) #El codigo http 201 significica exitoso y creado, en este caso devolvera 201 si se creo exitosamente el usuario tambien creamos un response model para que en la documentacion en el apartado de responses se pueda ver que devuelve esta peticion
async def user (user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code= 404, detail="El Usuario ya existe en el listado") #Para lanzar un error directamente, retornamos con raise
    else:
        user_list.append(user)
        return user

#Operacion PUT, Si Deseamos actualizar datos en la API es posible hacerlo con el metodo PUT
#Este metodo nos sirve para actualizar datos de la api como un usuario en nuestro caso

@router.put("/")
async def user (user: User):
    
    found = False
    #Aca iteramos una busqueda en la lista de usuarios para obtener el id del usuario que se va a actualizar
    for index, saved_user in enumerate(user_list):
        if saved_user.id == user.id:
            user_list[index] = user # reemplaza el index del usuario encontrado por el nuevo usuario ya editado
            found = True
    if not found:
        return {"Error":  "No se ha actualizado el usuario"}
    else:
        return user

#Operacion DELETE Si queremos eliminar datos del API con Utilizar DELETE es suficiente
#Este metodo nos permite eliminar un dato o un usuario de nuestro listado

@router.delete("/{id}")
async def user (id: int):
    
    found = False
    
    for index, saved_user in enumerate(user_list):
        if saved_user.id == id:
            del user_list[index]
            found = True
            return {"Mensaje": "Eliminacion exitosa"}
            
        if not found:
            return{"Error":  "No se ha eliminado el usuario"}


#Status code

# Existen diferentes codigos http, es importante revisarlos o aprenderlos a la hora de trabajar con API's ya sea en la doc de FastApi
# o en la MDN, aqui en fast api es posible, que una peticion devuelva a parte de datos, un codigo implementando el parametro status code

