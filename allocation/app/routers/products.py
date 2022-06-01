from typing import List

from app.adapters import repository
from app.adapters.orm import get_db
from app.domain import models
from app.service_layer import services, unit_of_work
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/v1/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{sku}", response_model=models.Product, tags=["products"])
def get_product(sku: str, db: Session = Depends(get_db)):
    db_product = services.get_product(sku=sku, repository=repository.SqlAlchemyRepository(session=db))
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.get("/", response_model=List[models.Product], tags=["products"])
def get_all_products(limit: int = 100, db: Session = Depends(get_db)):
    return services.get_all_products(limit=limit, uow=unit_of_work.SqlAlchemyUnitOfWork(session=db))
