from datetime import datetime
from typing import Optional

from pydantic import BaseModel, NonNegativeInt, PositiveInt


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationDB(DonationCreate):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationsDB(DonationCreate):
    invested_amount: NonNegativeInt
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]
    user_id: int
    id: int

    class Config:
        orm_mode = True
