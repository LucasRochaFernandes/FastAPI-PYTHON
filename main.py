from database import engine, SessionLocal
import models
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session

app = FastAPI(docs_url="/docs", redoc_url="/redoc")
models.Base.metadata.create_all(bind=engine)

class ChoiceBase(BaseModel):
  choiceText: str
  isCorrect: bool
class QuestionBase(BaseModel):
  questionText: str
  choices: List[ChoiceBase]
  
def getDb():
  db = SessionLocal()
  try: 
    yield db
  finally:
    db.close()
    
@app.get("/questions/{questionId}")
async def getQuestions(questionId: int, db: Session = Depends(getDb)):
  question = db.query(models.Questions).filter(models.Questions.id == questionId).first()
  if not question:
    raise HTTPException(status_code=404, detail='Question not found')
  return question

@app.get("/questions/{questionId}/choices")
async def readChoices(questionId: int, db: Session = Depends(getDb)):
  choices = db.query(models.Choices).filter(models.Choices.question_id == questionId)
  if not choices:
    raise HTTPException(status_code=404, detail='Choices not found')
  return choices  
  
@app.post("/questions")
async def createQuestions(data: QuestionBase, db: Session = Depends(getDb)):
    question = models.Questions(question_text=data.questionText)
    db.add(question)
    db.commit()
    db.refresh(question)
    for choiceInData in data.choices:
      choice = models.Choices(choice_text=choiceInData.choiceText, is_correct=choiceInData.isCorrect, question_id=question.id)
      db.add(choice)
    db.commit()
    return question
      
  