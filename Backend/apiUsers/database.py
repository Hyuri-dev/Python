from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

#Creamos el archivo de la BD
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

TURSO_DB_URL = os.environ.get("TURSO_DATABASE_URL")
TOKEN_DB = os.environ.get("TURSO_AUTH_TOKEN")


#Creamos un motor de SQLALCHEMY
engine = create_engine(
    "sqlite+libsql:///embedded.db",
        connect_args={
            "auth_token": TURSO_DB_URL,
            "sync_url": TOKEN_DB,
        },
)

# engine = create_engine (TURSO_DB_URL, connect_args= {"auth_token":TOKEN_DB},) # el connect args solo aplica para SQLITE

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind= engine)  

#Crear una clase Base que sera  la base para nuestros modelos

Base = declarative_base()