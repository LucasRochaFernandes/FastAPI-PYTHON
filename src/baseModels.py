from typing import List
from pydantic import BaseModel

class ChoiceRequest(BaseModel):
  choiceText: str
  isCorrect: bool
class QuestionRequest(BaseModel):
  questionText: str
  choices: List[ChoiceRequest]
  
class UsersRequest(BaseModel):
  name: str
  email: str
  password: str

class AuthenticateRequest(BaseModel):
  email: str
  password: str

class Token(BaseModel):
  access_token: str
  tokenType: str