from typing import List, Optional

from beanie import Document
from pydantic import BaseModel, Field


class AwardLink(BaseModel):
    lien: str
    titre: str


class AwardImage(BaseModel):
    url: str
    key: str
    alt: str


class Award(Document):
    titre: str
    rang: int = 0
    image: Optional[AwardImage] = None

    datedebut: Optional[str] = None
    datefin: Optional[str] = None

    chapo: Optional[str] = None
    contenu: Optional[str] = None 

    liens: List[AwardLink] = Field(default_factory=list)
    images: List[AwardImage] = Field(default_factory=list)

    class Settings:
        name = "awards"
