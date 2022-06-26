from app2.domain.models import Base
from fastapi import FastAPI

from .database import SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
