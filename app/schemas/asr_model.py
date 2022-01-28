from enum import Enum
from pydantic import BaseModel
from datetime import datetime


class Lang(str, Enum):
    FR = "french"
    EN = "english"
    DE = "german"
    PT = "portuguese"


class AsrModelBase(BaseModel):
    label: str
    description: str
    lang: str


class AsrModelCreate(AsrModelBase):
    pass


class AsrModel(AsrModelBase):
    id: int
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True
