from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from datetime import datetime
from bson import ObjectId


class Client(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )
    
    id: Optional[str] = Field(default=None, validation_alias="_id")
    image_url: str
    name: str
    description: str
    designation: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator('id', mode='before')
    @classmethod
    def validate_id(cls, v):
        if v is None:
            return None
        if isinstance(v, ObjectId):
            return str(v)
        return str(v)


class ClientCreate(BaseModel):
    name: str
    description: str
    designation: str


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    designation: Optional[str] = None

