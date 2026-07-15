from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,TEXT, create_engine

app = FastAPI()

create_engine()

DATABASE_URL= 'DB_URL'

engine = create_engine(DATABASE_URL) 

sessionLocal = sessionmaker(autocommit = False, autoflaush= False, bind=engine)
db = sessionLocal()

class userCreate (BaseM odel):
    name: str
    email: str
    password: str

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(TEXT, primary_key= True)
    name = Column (VARCHAR(100))
    email = Column(VARCHAR(100))
    password= Column(LargeBinary)

@app.post ('/sigup')
def signupUser(user: userCreate):
    print (user.name)
    print(user.email)
    print (user.password)
    #extract inputs from the user

    pass