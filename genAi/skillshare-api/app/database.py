from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool
import os
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    # connect_args={"check_same_thread": False}, poolclass=StaticPool,  # For Sqlite (locally)
    echo=True  # For Postgress (Production)
)

def create_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
