from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_pwd = os.getenv("DB_PWD")
db_host = os.getenv("DB_HOST")
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_pwd}@{db_host}/{db_name}"

engine = create_engine(
    # SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}    # Apenas para Sqlite
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()