from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

#Nombre de la base de datos
BD = "usuarios.db"
url = f"sqlite:///{BD}"
connect_args = {"check_same_thread": False}

engine = create_engine(url,connect_args= connect_args)

Session = sessionmaker(bind= engine)

session = Session()

# SesionLocal = sessionmaker(autocommit = False, autoflush= False, bind= engine)

Base = declarative_base()