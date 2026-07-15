from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, TEXT, VARCHAR, LargeBinary, create_engine
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(TEXT, primary_key=True)
    name = Column(VARCHAR(100))
    email = Column(VARCHAR(100))
    password = Column(LargeBinary)

@app.post("/signup")
def signup_user(user: UserCreate):
    print(user.name)
    print(user.email)
    print(user.password)
    return {"message": "received"}

Base.metadata.create_all(bind=engine)
