from pydantic import BaseModel
from typing import Optional

class QuestionBase(BaseModel):
    title: str
    content: str
    answer: Optional[str] = None

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int

    class Config:
        from_attributes = True

class AnswerUpdate(BaseModel):
    answer: str