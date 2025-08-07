import db
from models import Producto

def run():
  producto = Producto(input('ingrese el nombre del producto'), float(input('ingrese el precio')))
  db.session.add(producto)
  db.session.commit()
  print(f"se creo el producto correctamente: {producto.id}")


if __name__ == '__main__':
  db.base.metadata.create_all(db.engine)
  run()