from pydantic import BaseModel, field_validator, Field
from typing import Optional

class MandiPriceData(BaseModel):
    state: str = Field(..., min_length=2)
    district: str = Field(..., min_length=2)
    market_name: str
    commodity: str
    min_price: float
    modal_price: float
    max_price: float

    @field_validator("max_price")
    def check_price_logic(cls, v, info):
        if "min_price" in info.data and v < info.data["min_price"]:
            raise ValueError("max_price cannot be lower than min_price")
        return v
