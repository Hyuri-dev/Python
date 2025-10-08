import db
from models import Users

def crear_usuario(usuario , contraseña):
  cursor = Users(usuario = usuario, password = contraseña)
  db.session.add(cursor)
  db.session.commit()
  print('usuario creado correctamente')

if __name__ == "__main__":
    db.Base.metadata.create_all(db.engine)
    
    crear_usuario(input("Ingrese un usuario: "), input("Ingrese una contraseña: "))