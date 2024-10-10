from fastapi import FastAPI
from db import models, database
from views import caching

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(caching.router)