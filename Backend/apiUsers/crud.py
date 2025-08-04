from sqlalchemy.orm import session
import models , schemas
from fastapi import HTTPException

def get_user ( db: session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_email ( db: session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users (db: session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user (db:session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    
    db_user = models.User(email = user.email, hashed_password = fake_hashed_password )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_items ( db: session, skip: int = 0 , limit: int = 100): # traemos todos los items empezando desde el primero hasta un maximo de 100 
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_user_item(db:session, item : schemas.ItemCrate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id = user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item (db:session, item_id: int, item: schemas.ItemCrate):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        return None
    
    for key, value in item.dict().items():
        setattr(db_item, key,value)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item (db: session, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        return False
    db.delete(db_item)
    db.commit()
    return True