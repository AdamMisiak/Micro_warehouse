from fastapi import FastAPI
from app.api.db import metadata, database, engine
from app.api.batches import batches

app = FastAPI()

metadata.create_all(engine)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app = FastAPI()

app.include_router(batches)