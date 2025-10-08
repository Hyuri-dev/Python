import db1
from modelos1 import Producto

def run():
  producto = Producto(input('ingrese el nombre del producto'), float(input('ingrese el precio')))
  db1.session.add(producto)
  db1.session.commit()
  print(f"se creo el producto correctamente: {producto.nombre}")
  
  
  
def listar ():
  consultar = db1.session.query(Producto).all()
  print(f'Productos: {consultar}')

def buscar (id):
  search = db1.session.get(Producto, id)
  print(search)
  return search

def eliminar (id):
  product = db1.session.get(Producto, id)
  if product is None:
    print("No encontrado")
  else:
    db1.session.delete(product)
    print("Eliminated successfully")
    db1.session.commit()

def editar (id):
  product = db1.session.get(Producto,id)
  if product is None:
    print("No encontrado")
    return
  
  product.nombre = input("Ingrese el nombre nuevo del producto: ")
  db1.session.commit()


if __name__ == '__main__':
  db1.base.metadata.create_all(db1.engine)
  run()
  listar()
  buscar(input("Ingrese el id: "))
  # eliminar(input("Ingrese el id: "))
  editar(input("Ingrese el id: "))
