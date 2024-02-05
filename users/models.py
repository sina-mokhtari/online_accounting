import datetime
from typing import List, Optional, TYPE_CHECKING

from fastapi import Depends, FastAPI, HTTPException, Query

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Relationship

from db_conf.myModel import (Model)

# from finance.models import CreditCard


class User(Model):
    __tablename__ = "users"
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)
    cards = Relationship("CreditCard", back_populates="owner")
