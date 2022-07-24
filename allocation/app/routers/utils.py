# pylint: disable=C0103
# invalid-name
from typing import List

from app.database import get_db
from app.domain import models, schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/v1/utils",
    tags=["Utils"],
    responses={404: {"description": "Not found"}},
)
