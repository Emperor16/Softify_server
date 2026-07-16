from fastapi import FastAPI, HTTPException

from routes import auth

app.include_router(auth.router, prefix= '/auth')

Base.metadata.create_all(bind=engine)
