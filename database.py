from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#sqlachemy database url
DATABASE_URL = "sqlite:///./books.db"

#Create database engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

#Create session
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()
