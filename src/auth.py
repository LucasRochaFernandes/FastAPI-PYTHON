from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


bcryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2Bearer = OAuth2PasswordBearer(tokenUrl='sessions')
  





  