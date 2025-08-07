import db
from models import Producto

def run():
  producto = Producto(input('ingrese el nombre del producto'), float(input('ingrese el precio')))
  db.session.add(producto)
  db.session.commit()
  print(f"se creo el producto correctamente: {producto.id}")
  
  
  
def listar ():
  consultar = db.session.query(Producto).all()
  print(f'Productos: {consultar}')

def buscar (id):
  search = db.session.get(Producto, id)
  print(search)
  return search

def eliminar (id):
  product = db.session.get(Producto, id)
  if product is None:
    print("No encontrado")
  else:
    db.session.delete(product)
    print("Eliminated successfully")
    db.session.commit()
    
    


if __name__ == '__main__':
  db.base.metadata.create_all(db.engine)
  # run()
  listar()
  buscar(input("Ingrese el id: "))
  eliminar(input("Ingrese el id: "))
  
