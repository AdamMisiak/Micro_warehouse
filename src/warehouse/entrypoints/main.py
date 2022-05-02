
from fastapi import FastAPI


from datetime import datetime

from warehouse.adapters import orm
from warehouse.service_layer import services, unit_of_work

app = FastAPI()
orm.start_mappers()

@app.get("/batches")
async def all():
    # batches = 
    return {"message": "Hello QWE"}

@app.post("/batches")
async def create():
    return {"message": "Hello QWE"}