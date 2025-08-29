# api/database/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = os.getenv(
#     "DATABASE_URL",
#     "postgresql+psycopg://user:password@localhost:5433/ad_finder_db"
# )

DATABASE_URL = "postgresql+psycopg2://user:G-8kdjf63c-c*x@db:5432/ad_finder_db"

engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
