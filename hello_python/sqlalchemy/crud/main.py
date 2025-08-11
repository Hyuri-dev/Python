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

def buscar (id):
  user = db.session.get(Usuarios, id)
  if user is None:
    print("Usuario no encontrado")
  print(f"Usuario: {user} producto: {user.productos}")
  return user

if __name__ == "__main__":
  db.base.metadata.create_all(db.engine)
  
  print("<--------------- INGRESE UNA OPCION --------------- > \n\n 1. Crear usuario y producto asociado al usuario \n 2. Buscar usuario \n 3. Crear Producto \n 4.Editar usuario \n 5.Editar producto \n 6.Eliminar usuario \n 7. Eliminar producto")
  
  opcion = int(input("Ingrese una opcion"))
  match (opcion):
    case 1:
      crear_usuario(input('Ingrese el nombre: ') , input('Ingrese la identificacion: '))
      response = input("¿ Desea añadir un producto al usuario ? Y/N: ")
      if response == ("Y"):
        
        crear_producto(input('Ingrese el nombre: ') , input('Ingrese descripcion:  '), input('Ingrese propietario si tiene: '))  
      else:
        print("Usuario creado con exito")
    case 2: 
      buscar(input("Ingrese el id del usuario"))