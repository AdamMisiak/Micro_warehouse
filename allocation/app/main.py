from fastapi import FastAPI
from app.api.db import metadata, database, engine
from app.api.batches import batches
from app.api.order_lines import order_lines

app = FastAPI()

metadata.create_all(engine)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app = FastAPI()

app.include_router(batches, prefix='/api/v1/batches', tags=['batches'])
app.include_router(order_lines, prefix='/api/v1/orderlines', tags=['order_lines'])