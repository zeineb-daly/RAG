from typing import Literal

from pydantic import BaseModel


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class QuestionRequest(BaseModel):
    question: str
    course: str | None = None  # None = search in every course
    history: list[Message] = []  # previous messages of the conversation
