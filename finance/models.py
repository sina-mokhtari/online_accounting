from typing import List, Optional
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from users.models import User
from sqlalchemy.orm import Relationship

from db_conf.myModel import Model


class CreditCard(Model):
    __tablename__ = "credit_cards"
    number = Column(String, nullable=False)
    type = Column(String, nullable=False)
    balance = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = Relationship("User", back_populates="cards")

#
# class CreditCardBase(SQLModel):
#     number: str
#     type: str
#     balance: int
#     owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
#
#
# class CreditCard(CreditCardBase, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
