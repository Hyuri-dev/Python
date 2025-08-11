from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

#Conector para mariadb
engine = create_engine("mariadb+mariadbconnector://root:aquiles@localhost:3306/mi_tienda")

Session = sessionmaker(bind= engine)

session = Session()

base = declarative_base()


