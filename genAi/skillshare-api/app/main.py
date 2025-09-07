from fastapi import FastAPI

from routes.auth_routes import auth_router
from routes.skill_routes import skill_router
from database import create_db

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(skill_router, prefix="/skills")

@app.on_event("startup")
def on_startup():
    create_db()
