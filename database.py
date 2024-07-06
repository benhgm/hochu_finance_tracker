from sqlalchemy import create_engine, Column, String, Float, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    item = Column(String, index=True)
    mode_of_payment = Column(String)
    credit_card = Column(String)
    category = Column(String)
    amount = Column(Float)
    date = Column(DateTime)

def get_engine(user_name: str):
    db_path = f"./databases/{user_name}.db"
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    DATABASE_URL = f"sqlite:///{db_path}"
    return create_engine(DATABASE_URL)

def get_session(user_name: str):
    engine = get_engine(user_name)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def create_user_database(user_name: str):
    engine = get_engine(user_name)
    Base.metadata.create_all(bind=engine)
