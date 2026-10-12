from uuid import UUID

from pydantic import BaseModel


class QuestionnaireShort(BaseModel):
    uid: UUID
    cod: int
    name: str


class AnswerOption(BaseModel):
    uid: UUID
    cod: int | None
    value: str | None


class QuestionOut(BaseModel):
    uid: UUID
    id: int | None
    order: int | None
    short_text: str | None
    text: str | None
    required: bool


class QuestionGroup(BaseModel):
    cod: int | None
    name: str | None
    questions: list[QuestionOut]


class QuestionnaireDetail(BaseModel):
    uid: UUID
    cod: int
    name: str
    answer_options: list[AnswerOption]
    groups: list[QuestionGroup]
