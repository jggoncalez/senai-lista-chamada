# backend-python/reset_tables.py
from app.database import engine, Base
from app.models import *  # importa todos os models

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
print("Tabelas recriadas!")