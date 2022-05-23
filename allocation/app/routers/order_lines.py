from app.adapters.orm import get_db
from app.domain import models
from app.service_layer import services
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/v1/order_lines",
    tags=["order_lines"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=models.OrderLine, tags=["order_lines"])
def create_order_lines(order_line: models.OrderLine, db: Session = Depends(get_db)):
    return services.create_order_line(db=db, order_line=order_line)
