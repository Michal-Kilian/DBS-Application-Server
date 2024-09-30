from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
import os


POSTGRES_USER: str = os.getenv("DATABASE_USER")
POSTGRES_PASSWORD = os.getenv("DATABASE_PASSWORD")
POSTGRES_SERVER: str = os.getenv("DATABASE_HOST", "localhost")
POSTGRES_PORT: str = os.getenv("DATABASE_PORT", 5432)
POSTGRES_DB: str = os.getenv("DATABASE_NAME", "dbs")
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


engine = create_engine(DATABASE_URL)
# engine = create_engine(f"postgresql://postgres:heslo@localhost:5432/dbs5")

Base = declarative_base()

Session = sessionmaker(bind=engine)
