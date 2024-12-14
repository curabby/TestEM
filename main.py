import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.models.models import Base
from db import engine
from fastapi import FastAPI
from v1.api import api_router

app = FastAPI()

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Подключение роутеров
app.include_router(api_router)
