from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Creamos el archivo de la BD
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

#Creamos un motor de SQLALCHEMY

engine = create_engine (SQLALCHEMY_DATABASE_URL, connect_args= {"check_same_thread": False}) # el connect args solo aplica para SQLITE

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind= engine)

#Crear una clase Base que sera  la base para nuestros modelos

Base = declarative_base()