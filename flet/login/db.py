from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Nombre de la base de datos
BD = "usuarios.db"
url = f"sqlite:///{BD}"
connect_args = {"check _same_thread": False}

engine = create_engine(url,connect_args)

SesionLocal = sessionmaker(autocommit = False, autoflush= False, bind= engine)

Base = declarative_base()