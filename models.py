from typing import List, Optional, Dict
from pydantic import BaseModel
from datetime import datetime


class Field(BaseModel):
    id: str
    ref: str
    type: str
    title: str
    properties: Optional[Dict]


class Ending(BaseModel):
    id: str
    ref: str
    title: str
    type: str
    properties: Optional[Dict]


class Definition(BaseModel):
    id: str
    title: str
    fields: List[Field]
    endings: List[Ending]


class FieldAnswer(BaseModel):
    id: str
    type: str
    ref: str


class Answer(BaseModel):
    type: str
    field: FieldAnswer
    text: Optional[str] = None
    email: Optional[str] = None
    boolean: Optional[bool] = None


class EndingReference(BaseModel):
    id: str
    ref: str


class FormResponse(BaseModel):
    form_id: str
    token: str
    landed_at: datetime
    submitted_at: datetime
    definition: Definition
    answers: List[Answer]
    ending: EndingReference


class Event(BaseModel):
    event_id: str
    event_type: str
    form_response: FormResponse
