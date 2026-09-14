from pydantic import BaseModel, Field, model_validator

class MandiPriceData(BaseModel):
    state: str = Field(..., min_length=2)
    district: str = Field(..., min_length=2)
    market_name: str
    commodity: str
    min_price: float = Field(..., ge=0)
    modal_price: float = Field(..., ge=0)
    max_price: float = Field(..., ge=0)

    @model_validator(mode="after")
    def check_price_logic(self):
        if not self.min_price <= self.modal_price <= self.max_price:
            raise ValueError("prices must satisfy min_price <= modal_price <= max_price")
        return self
