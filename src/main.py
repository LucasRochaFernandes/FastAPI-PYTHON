from datetime import datetime, timedelta
from src.baseModels import AuthenticateRequest, QuestionRequest, UsersRequest
from fastapi.responses import JSONResponse
import src.database.models as models
from fastapi import FastAPI, HTTPException
from starlette import status
from src.dependencies import dbDependency
from src.auth import bcryptContext
from src.database.index import migrate
from jose import jwt

from src.dependencies import authDependency
from src.env import algorithmJWT, secretKeyJWT

app = FastAPI(docs_url="/docs", redoc_url="/redoc")
migrate()

@app.get("/questions/{questionId}")
async def getQuestions(questionId: int, db: dbDependency):
  question = db.query(models.Questions).filter(models.Questions.id == questionId).first()
  if not question:
    raise HTTPException(status_code=404, detail='Question not found')
  return question

@app.get("/questions/{questionId}/choices")
async def readChoices(questionId: int, db: dbDependency):
  choices = db.query(models.Choices).filter(models.Choices.question_id == questionId)
  if not choices:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Choices not found')
  return choices  
  
@app.post("/questions")
async def createQuestions(data: QuestionRequest, db: dbDependency):
    question = models.Questions(question_text=data.questionText)
    db.add(question)
    db.commit()
    db.refresh(question)
    for choiceInData in data.choices:
      choice = models.Choices(choice_text=choiceInData.choiceText, is_correct=choiceInData.isCorrect, question_id=question.id)
      db.add(choice)
    db.commit()
    db.refresh(question)
    return question
      
@app.post("/users", status_code=status.HTTP_201_CREATED)
async def createUser(data: UsersRequest, db: dbDependency):
  usersInDatabase = db.query(models.Users).filter(models.Users.email == data.email).first()
  if usersInDatabase:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email Already Registered')
  hashPassword = bcryptContext.hash(data.password)
  createUserModel = models.Users(email=data.email, password=hashPassword, name=data.name)
  db.add(createUserModel)
  db.commit()
  db.refresh(createUserModel)
  return createUserModel

@app.post('/sessions', status_code=status.HTTP_201_CREATED)
async def authenticate(data: AuthenticateRequest, db: dbDependency):
   user = db.query(models.Users).filter(models.Users.email == data.email).first()
   if not user:
     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Credentials')
   isMatch = bcryptContext.verify(data.password, user.password)
   if not isMatch:
     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Credentials')
   encode = {'sub': str(user.id)}
   expires = datetime.utcnow() + timedelta(days=3)
   encode.update({'exp': expires})
   access_token = jwt.encode(encode, secretKeyJWT, algorithm=algorithmJWT )
   content = {'access_token': access_token, 'token_type': 'bearer'}
   response = JSONResponse(content=content)
   response.set_cookie(key="access_token", value=access_token, path='/', httponly=True)
   return response

@app.get('/profile', status_code=status.HTTP_200_OK)
async def profile(auth: authDependency, db: dbDependency):
  user = db.query(models.Users).filter(models.Users.id == auth['userId']).first()
  return user