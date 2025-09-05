from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import mariadb

#Conector para mariadb
engine = create_engine("mariadb+mariadbconnector://jodomode_jpadmin:xM0-=fdZvO,8JjnD@147.135.104.21:3306/jodomode_example", pool_pre_ping=True)

Session = sessionmaker(bind= engine)

session = Session()

base = declarative_base()
