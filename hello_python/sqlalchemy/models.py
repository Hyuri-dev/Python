import db
from sqlalchemy import Column, Integer, String , Float

#modelo de nuestra tabla productos

class Producto(db.base):
  __tablename__ = 'producto'
  id = Column(Integer, primary_key = True )
  nombre = Column(String, nullable = False)
  precio = Column(Float)
  
  def __init__(self, nombre, precio):
    self.nombre = nombre
    self.precio = precio
    
  def __repr__(self):
    return f'producto({self.nombre}, {self.precio})' #Aca representamos de una manera mas formal nuestros datos
  
  def __str__(self):
    return f"{self.nombre} - {self.precio}" #el str nos traera los datos que mandemos a llamar por print.