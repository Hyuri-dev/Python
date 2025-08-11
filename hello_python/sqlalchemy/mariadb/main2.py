import db2
from models2 import Usuarios


def crear_usuario (nombre, identificacion):
  cursor = Usuarios(nombre, identificacion)
  db2.session.add(cursor)
  db2.session.commit()
  print('Datos creados exitosamente!')



if __name__ == "__main__":
  db2.base.metadata.create_all(db2.engine)
  crear_usuario(input("Ingrese un nombre: "), int(input("Ingrese la identificacion: ")))