from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from src.database.index import getDb
from src.middlewares import verifyJWT

authDependency = Annotated[dict, Depends(verifyJWT)]
dbDependency = Annotated[Session, Depends(getDb)]