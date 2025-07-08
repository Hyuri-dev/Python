from fastapi import APIRouter

router = APIRouter(prefix="/products", tags= ["products"] ,responses= { 404: {"Message": "No encontrado"}}) #Los prefijos en los routers nos sirven para que automaticamente al llamar a la api se posicione en /routers, asi no hace falta repetir el path en cada una de las peticiones / acciones
# El tag nos agrupa en la documentacion las peticiones que utiliza el api de productos. 
products_list = ["Producto 1" , "Producto 2" , "Producto 3" , "Producto 4"]

@router.get("/")
async def products():
    return products_list

@router.get("/{id}")
async def products(id: int):
    return products_list[id]