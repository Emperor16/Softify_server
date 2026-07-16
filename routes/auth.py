from database import SessionLocal, get_db
from fastapi import APIRouter, HTTPException, Depends
import bcrypt
from sqlalchemy.orm import Session
import uuid
from models.user import User
from pydantic_schemas.user_create import UserCreate
from pydantic_schemas.user_login import userLogin

router = APIRouter()

@router.post("/signup")
def signup_user(user: UserCreate, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.email == user.email).first()

    if user_db:
        raise HTTPException(status_code=400, detail="User with the same email already exists")

    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())

    new_user = User(
        id=str(uuid.uuid4()),
        name=user.name,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "user created",
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "password": new_user.password.decode()
    }

@router.post("/login")
def login_user(user: userLogin, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.email == user.email).first()

    if not user_db:
        raise HTTPException(status_code=400, detail="User with this email is not found")

    if not bcrypt.checkpw(user.password.encode(), user_db.password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    return {
        "message": "login successful",
        "id": user_db.id,
        "name": user_db.name,
        "email": user_db.email
    }