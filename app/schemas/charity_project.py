from datetime import datetime
from typing import Optional

from pydantic import Field, PositiveInt, NonNegativeInt, Extra  # BaseModel, validator

from .base import ProjectBaseModel


class CharityProjectBase(ProjectBaseModel):
    name: str = Field(None, min_length=1, max_length=100)
    description: str = Field(None, min_length=1)
    invested_amount: NonNegativeInt
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]


class CharityProjectCreate(ProjectBaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt = Field(...,)


class CharityProjectUpdate(ProjectBaseModel):
    name: str = Field(None, min_length=1, max_length=100)
    description: str = Field(None, min_length=1)
    full_amount: PositiveInt = Field(None,)

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    id: int

    class Config:
        orm_mode = True
