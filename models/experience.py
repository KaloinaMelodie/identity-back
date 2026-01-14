from typing import List, Optional

from beanie import Document
from pydantic import BaseModel, Field


class ExperienceLink(BaseModel):
    lien: str
    titre: str


class Experience(Document):
    titre: str
    rang: int = 0
    organisation: Optional[str] = None

    datedebut: Optional[str] = None
    datefin: Optional[str] = None

    chapo: Optional[str] = None
    contenu: Optional[str] = None 

    liens: List[ExperienceLink] = Field(default_factory=list)

    class Settings:
        name = "experiences"
