from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR, LargeBinary, create_engine
from dotenv import load_dotenv
import os
import uuid
import bcrypt

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(100))
    email = Column(VARCHAR(100))
    password = Column(LargeBinary)

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

app = FastAPI()

@app.post("/signup")
def signup_user(user: UserCreate):
    db = SessionLocal()
    user_db = db.query(User).filter(User.email == user.email).first()

    # FIXED: correct exception class + correct logic
    if user_db:
        db.close()
        raise HTTPException(400,"User with the same email already exists")

    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

    return {"message": "user created", "id": new_user.id}

Base.metadata.create_all(bind=engine)
