from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from typing import Optional
from datetime import datetime
from bson import ObjectId


class Contact(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )
    
    id: Optional[str] = Field(default=None, validation_alias="_id")
    full_name: str
    email: EmailStr
    mobile_number: str
    city: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator('id', mode='before')
    @classmethod
    def validate_id(cls, v):
        if v is None:
            return None
        if isinstance(v, ObjectId):
            return str(v)
        return str(v)


class ContactCreate(BaseModel):
    full_name: str
    email: EmailStr
    mobile_number: str
    city: str

