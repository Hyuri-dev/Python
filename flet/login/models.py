from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from db import Base

class Users (Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(primary_key= True, index=True)
    usuario: Mapped[str] = mapped_column(index=True)
    password: Mapped[str] = mapped_column()
    created_date: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    