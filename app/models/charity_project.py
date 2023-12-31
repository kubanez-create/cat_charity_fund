from sqlalchemy import Column, String, Text

from .base import BaseModel


class CharityProject(BaseModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text(1), nullable=False)
