from fastapi import FastAPI

from app.api.api_v1.api import api_router
from app.db.base import engine
from app.models import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router)
