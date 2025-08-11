import db2
from sqlalchemy import Column, Integer, String , Float , DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func



class Usuarios(db2.base):
  __tablename__= 'usuarios'
  id = Column (Integer, primary_key= True, index = True)
  nombre = Column(String(30), nullable= False, index= True)
  identificacion = Column(String(8), unique=True, index= True)
  fecha_creacon = Column(DateTime(timezone=True), server_default=func.now())
  
  def __init__(self, nombre , identificacion):
    self.nombre = nombre
    self.identificacion = identificacion
    
  def __repr__(self):
    return f'USUARIO: ({self.nombre}) IDENTIFICACION:({self.identificacion})'
  
  def __str__(self):
    return f'{self.nombre} {self.identificacion}'