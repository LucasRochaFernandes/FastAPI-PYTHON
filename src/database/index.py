from fastapi import Depends
from src.env import databaseURL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Annotated
import src.database.models as models
from sqlalchemy.orm import Session

engine = create_engine(databaseURL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def migrate():
  models.Base.metadata.create_all(bind=engine)

def getDb():
  db = SessionLocal()
  try: 
    yield db
  finally:
    db.close()

dbDependency = Annotated[Session, Depends(getDb)]