
from fastapi import FastAPI


from datetime import datetime

from adapters import orm
from service_layer import services, unit_of_work

app = FastAPI()
orm.start_mappers()

@app.get("/batches")
async def all():
    # batches = 
    return {"message": "Hello QWE"}

@app.post("/batches")
async def create():
    return {"message": "Hello QWE"}