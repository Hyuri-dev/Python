from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite:///productos.sqlite')

Session = sessionmaker(bind= engine)

session = Session ()

base = declarative_base()

