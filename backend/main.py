from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 更新CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # 明确指定前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/questions/", response_model=List[schemas.Question])
def read_questions(db: Session = Depends(get_db)):
    questions = db.query(models.Question).all()
    # 为每个问题添加是否有答案的标记
    for question in questions:
        question.has_answer = bool(question.answer)
    return questions

# 搜索接口需要放在具体 ID 匹配之前
@app.get("/questions/search/")
def search_questions(keyword: str, db: Session = Depends(get_db)):
    questions = db.query(models.Question).filter(
        models.Question.title.contains(keyword) |
        models.Question.content.contains(keyword)
    ).all()
    # 为搜索结果添加是否有答案的标记
    for question in questions:
        question.has_answer = bool(question.answer)
    return questions

@app.post("/questions/", response_model=schemas.Question)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    db_question = models.Question(
        title=question.title,
        content=question.content,
        answer=question.answer
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

@app.get("/questions/{question_id}", response_model=schemas.Question)
def read_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@app.put("/questions/{question_id}/answer", response_model=schemas.Question)
def update_answer(question_id: int, answer_update: schemas.AnswerUpdate, db: Session = Depends(get_db)):
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    question.answer = answer_update.answer
    db.commit()
    db.refresh(question)
    return question