from pydantic import BaseModel, field_validator
from datetime import datetime
import re


class TrackingResponse(BaseModel):
    item_number: str
    status: str
    location: str | None
    updated_at: datetime

    class Config:
        from_attributes = True


class TrackingBatchRequest(BaseModel):
    item_numbers: list[str]

    @field_validator("item_numbers")
    @classmethod
    def validate_item_numbers(cls, v):
        if len(v) > 10:
            raise ValueError("A maximum of 10 items can be entered at a time")
        pattern = re.compile(r"^[A-Z]{2}\d{9}[A-Z]{2}$")
        for item in v:
            if not pattern.match(item):
                raise ValueError(f"Invalid item number format: {item}")
        return v
