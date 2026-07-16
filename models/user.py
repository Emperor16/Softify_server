from models.base import Base
from sqlalchemy import Column, VARCHAR, LargeBinary


class User(Base):
    __tablename__ = "users"
    id = Column(VARCHAR(36), primary_key=True, index=True)   # FIXED: UUID-compatible
    name = Column(VARCHAR(100))
    email = Column(VARCHAR(100))
    password = Column(LargeBinary)

