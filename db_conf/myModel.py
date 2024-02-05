from datetime import datetime
from sqlalchemy import create_engine, Column, DateTime, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Model(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())
    is_deleted = Column(Boolean, default=False)