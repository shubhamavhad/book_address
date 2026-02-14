import re
from typing import Optional
from pydantic import BaseModel, Field, field_validator

#Schemas for address book application
class AddressBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    street: str = Field(..., min_length=2, max_length=150)
    city: str = Field(..., min_length=2, max_length=100)

    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

    #Remove leading/trailing spaces
    @field_validator("name", "street", "city")
    @classmethod
    def no_empty_strings(cls, value: str):
        value = value.strip()
        if not value:
            raise ValueError("Field cannot be empty or whitespace")
        return value

    #Only allow letters & spaces in city
    @field_validator("city")
    @classmethod
    def validate_city(cls, value: str):
        if not re.match(r"^[A-Za-z\s]+$", value):
            raise ValueError("City must contain only letters and spaces")
        return value

class AddressCreate(AddressBase):
    pass

class AddressUpdate(BaseModel):
    name: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
class AddressResponse(AddressBase):
    id: int

    model_config = {
        "from_attributes": True
    }
