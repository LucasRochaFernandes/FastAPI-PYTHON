import os 
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv()

load_dotenv(dotenv_path)

databaseURL = os.getenv("DATABASE_URL_PG")
secretKeyJWT = os.getenv("SECRET_KEY")
algorithmJWT = os.getenv("ALGORITHM")
