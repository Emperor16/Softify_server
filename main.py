from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, VARCHAR, LargeBinary, create_engine
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
    id = Column(VARCHAR(36), primary_key=True, index=True)   # FIXED: UUID-compatible
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

    if user_db:
        db.close()
        raise HTTPException(status_code=400, detail="User with the same email already exists")

    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())

    # FIXED: UUID assigned properly
    new_user = User(
        id=str(uuid.uuid4()),
        name=user.name,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

    return {
    "message": "user created",
    "id": new_user.id,
    "name": new_user.name,
    "email": new_user.email,
    "password": new_user.password.decode()  # hashed password as string
}


Base.metadata.create_all(bind=engine)
