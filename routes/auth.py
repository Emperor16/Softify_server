from database import SessionLocal
from fastapi import APIRouter, HTTPException
import bcrypt
from models.user import User
from pydantic_schemas.user_create import UserCreate
from sqlalchemcy import session
from database import get_db
import uuid
router = APIRouter()

@router.post("/signup")
def signup_user(user: UserCreate, db:session= Depends(get_db)):
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
