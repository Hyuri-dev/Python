from sqlalchemy import Column, ForeignKey, Integer, String,Text, DateTime # importamos los tipos de columnas para las tablas
from sqlalchemy.orm import relationship # Para relacionar tablas o nuestras clases en este caso
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
class User (Base): # Creamos la tabla usuario 
    __tablename__ = "users" 
    # id: Mapped[int] = mapped_column(primary_key=True, index=True)
    id  = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    #Relacion con la tabla users y items de uno a muchos
    items =  relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index= True)
    title = Column(String, index=True)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    #Relacion con la tabla items y usuarios de uno a uno 
    owner = relationship("User", back_populates="items")


