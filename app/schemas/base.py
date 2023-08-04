from pydantic import BaseModel, PositiveInt  # validator, Field


class ProjectBaseModel(BaseModel):
    full_amount: PositiveInt
