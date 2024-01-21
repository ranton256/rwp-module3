from typing import List

from pydantic import BaseModel, HttpUrl


class QuizItem(BaseModel):
    question: str
    answer: str


class Quiz(BaseModel):
    title: str
    items: List[QuizItem]


class QuizInfo(BaseModel):
    name: str
    link: HttpUrl


"""
# Example usage
example_quiz = Quiz(items=[
  {"question": "What does a volt represent?",
   "answer":
    "the electromotive force required to drive an amp of current thru one ohm."},
  # ... add other questions and answers
])
"""
