from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from dotenv import load_dotenv
import os
import urllib

load_dotenv()

_server   = os.getenv("DB_SERVER")
_database = os.getenv("DB_NAME")
_user     = os.getenv("DB_USER")
_password = os.getenv("DB_PASSWORD")

if not all([_server, _database, _user, _password]):
    raise RuntimeError("Variáveis de banco não definidas no .env (DB_SERVER, DB_NAME, DB_USER, DB_PASSWORD)")

_odbc = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={_server};"
    f"DATABASE={_database};"
    f"UID={_user};"
    f"PWD={_password};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=yes;"
    f"Connection Timeout=30;"
)

DATABASE_URL = "mssql+pyodbc:///?odbc_connect=" + urllib.parse.quote_plus(_odbc)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
