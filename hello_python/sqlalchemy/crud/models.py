import db
from sqlalchemy import Column, Integer, String , Float , DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Usuarios(db.base):
  __tablename__ = 'usuarios'
  id = Column(Integer, primary_key= True, index= True)
  nombre = Column(String, nullable= False, index= True)
  identificacion = Column(Integer, unique= True, index=True)
  fecha_creación = Column(DateTime(timezone=True), server_default=func.now())
  
  productos = relationship("Productos", back_populates="propietario")
  
  def __init__(self, nombre, identificacion):
    self.nombre = nombre
    self.identificacion = identificacion
    
  
  def __repr__(self):
    return f'Usuario: ({self.nombre} identificacion: {self.identificacion})'
  
  def __str__(self):
    return f'{self.nombre} {self.identificacion}'


class Productos (db.base):
  __tablename__ = 'productos'
  id = Column(Integer, primary_key= True, index=True)
  nombre = Column(String, nullable=False ,index= True)
  descripcion = Column(String, nullable=True, index=True)
  id_propietario = Column(Integer,ForeignKey ("usuarios.id"), nullable= True)
  fecha_creacion = Column(DateTime(timezone=True), server_default=func.now() )
  
  propietario = relationship("Usuarios", back_populates="productos")
  
  def __init__(self, nombre, descripcion, id_propietario):
    self.nombre = nombre
    self.descripcion = descripcion
    self.id_propietario = id_propietario

  
  def __repr__(self):
    return f'Producto ({self.nombre} descripcion: {self.descripcion})'
  
  def __str__(self):
    return f'{self.nombre} {self.descripcion}'
