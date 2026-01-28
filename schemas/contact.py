from typing import List, Optional

from pydantic import BaseModel, Field
from beanie import PydanticObjectId


class ContactBase(BaseModel):
    name: str
    email: Optional[str] = None
    date: Optional[str] = None
    contenu: Optional[str] = None 



class ContactCreate(BaseModel):
    name: str
    email: Optional[str] = None
    date: Optional[str] = None
    contenu: Optional[str] = None 


class ContactUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    date: Optional[str] = None
    contenu: Optional[str] = None


class Contact(ContactBase):
    id: PydanticObjectId

    class Config:
        json_encoders = {PydanticObjectId: str}
