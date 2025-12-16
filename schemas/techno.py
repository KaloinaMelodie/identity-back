from typing import List, Optional

from pydantic import BaseModel, Field
from beanie import PydanticObjectId


class TechnoLinkBase(BaseModel):
    lien: str
    titre: str


class TechnoImageIn(BaseModel):
    image: str  # base64 or data url
    alt: str

class TechnoImageOut(BaseModel):
    url: str
    key: str
    alt: str

class TechnoBase(BaseModel):
    titre: str
    categorie: str
    image: Optional[TechnoImageOut] = None
    chapo: Optional[str] = None

class TechnoCreate(BaseModel):
    titre: str
    categorie: str
    image: Optional[TechnoImageIn] = None
    chapo: Optional[str] = None


class TechnoUpdate(BaseModel):
    titre: Optional[str] = None
    categorie: Optional[str] = None
    image: Optional[TechnoImageIn] = None
    chapo: Optional[str] = None


class Techno(TechnoBase):
    id: PydanticObjectId

    class Config:
        json_encoders = {PydanticObjectId: str}
