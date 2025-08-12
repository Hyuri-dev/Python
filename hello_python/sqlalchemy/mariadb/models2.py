import db2
from sqlalchemy import Column, Integer, String , Float , DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func



class Usuarios(db2.base):
  __tablename__= 'usuarios'
  id = Column (Integer, primary_key= True, index = True)
  nombre = Column(String(30), nullable= False, index= True)
  identificacion = Column(String(8), unique=True, index= True)
  fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
  
  productos = relationship("Productos", back_populates="propietario")
  
  def __init__(self, nombre , identificacion):
    self.nombre = nombre
    self.identificacion = identificacion
    
  def __repr__(self):
    return f'USUARIO: ({self.nombre}) IDENTIFICACION:({self.identificacion})'
  
  def __str__(self):
    return f'{self.nombre} {self.identificacion}'


class Productos (db2.base):
  __tablename__ = 'productos'
  id = Column(Integer, primary_key=True, index=True)
  nombre = Column(String(30), nullable=False, index=True)
  descripcion = Column(String(200), nullable=True)
  precio = Column(Integer, nullable= False)
  id_propietario = Column(Integer, ForeignKey ("usuarios.id"), nullable= True)
  fecha_creacion = Column(DateTime(timezone= True), server_default=func.now())
  
  propietario = relationship("Usuarios", back_populates="productos")
  
  def __init__(self, nombre, descripcion, precio ,id_propietario):
    self.nombre = nombre
    self.descripcion = descripcion
    self.precio = precio
    self.id_propietario = id_propietario
  
  def __repr__(self):
    return f'PRODUCTO: [{self.nombre}] DESCRIPCION: [{self.descripcion}] PRECIO: [{self.precio}]'
  
  def __str__(self):
    return f'{self.nombre} {self.descripcion} {self.precio}'