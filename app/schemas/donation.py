from typing import Optional
from datetime import datetime

from pydantic import NonNegativeInt  # BaseModel, root_validator, validator, Extra,Field, PositiveInt, 

from .base import ProjectBaseModel


class DonationBase(ProjectBaseModel):
    invested_amount: NonNegativeInt
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]
    comment: Optional[str]
    user_id: int


class DonationCreate(ProjectBaseModel):
    comment: Optional[str]


class DonationDB(DonationCreate):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationsDB(DonationBase):
    id: int

    class Config:
        orm_mode = True
