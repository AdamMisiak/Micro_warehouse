from app.adapters.orm import get_db
from app.domain import models
from app.service_layer import services, unit_of_work
from app.utils import exceptions
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/v1/order_lines",
    tags=["order_lines"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=models.OrderLine, tags=["order_lines"])
def create_order_lines(order_line: models.OrderLine, db: Session = Depends(get_db)):
    db_order_line = services.get_order_line(db, order_line_id=order_line.id)
    if db_order_line:
        raise HTTPException(status_code=400, detail="Order line with this id already exists")
    return services.create_order_line(db=db, order_line=order_line)


@router.post("/allocate", tags=["order_lines"])
def allocate_batches(order_line: models.OrderLine, db: Session = Depends(get_db)):
    try:
        batch_reference = services.allocate(order_line, uow=unit_of_work.SqlAlchemyUnitOfWork(session=db))
    except (exceptions.OutOfStock, exceptions.InvalidSku) as e:
        return {"message": str(e)}, 400

    return {"batch_reference": batch_reference}, 201
