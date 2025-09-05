from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import mariadb

usuario="jodomode_jpadmin"
contraseña="soulkidd0809@"
host = "147.135.104.21"
db = "jodomode_example"

conn_string = f"mariadb+mariadbconnector://{usuario}:{contraseña}@{host}:3306/{db}"

#Conector para mariadb
engine = create_engine(conn_string, echo = True)
Session = sessionmaker(bind= engine)

session = Session()

base = declarative_base()
