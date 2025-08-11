import db
from models import Usuarios , Productos


def crear_usuario (nombre, identificacion):
  usuario = Usuarios(nombre, identificacion)
  db.session.add(usuario)
  db.session.commit()
  print(f'Se creo el usuario correctamente: {usuario.nombre}')

def crear_producto (nombre, descripcion, propietario):
  producto = Productos(nombre,descripcion,propietario)
  db.session.add(producto)
  db.session.commit()
  print(f'Se creo el siguiente producto correctamente: {producto.nombre}')
  

if __name__ == "__main__":
  db.base.metadata.create_all(db.engine)
  crear_usuario(input('Ingrese el nombre: ') , input('Ingrese la identificacion: '))
  response = input("¿ Desea añadir un producto al usuario ? Y/N: ")
  if response == ("Y"):
    crear_producto(input('Ingrese el nombre: ') , input('Ingrese descripcion:  '), input('Ingrese propietario si tiene: '))
    
  else:
    print("Usuario creado con exito")


