import db2
from models2 import Usuarios , Productos


def crear_usuario (nombre, identificacion):
  cursor = Usuarios(nombre, identificacion)
  db2.session.add(cursor)
  db2.session.commit()
  print('Datos creados exitosamente!')

def crear_producto (nombre , descripcion, precio, propietario):
  cursor = Productos(nombre , descripcion, precio, propietario)
  db2.session.add(cursor)
  db2.session.commit()
  print(f'Se ha creado el producto: {cursor.nombre} con un precio de: {cursor.precio} propietario: {cursor.propietario}')



if __name__ == "__main__":
  db2.base.metadata.create_all(db2.engine)
  
  option = int(input("Ingrese una opcion: "))
  
  match (option):
    case 1 :
      crear_usuario(input("Ingrese un nombre: "), int(input("Ingrese la identificacion: ")))
    
    case 2:
      crear_producto(input("Ingrese el nombre del producto: "), input("Ingrese la descripcion del producto (opcional): "), int(input("Ingrese el precio del producto: ")), input("ingrese el id del propietario si tiene: "))