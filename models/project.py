from typing import List, Optional

from beanie import Document
from pydantic import BaseModel, Field


class ProjectLink(BaseModel):
    lien: str
    titre: str


class ProjectImage(BaseModel):
    url: str
    key: str
    alt: str


class Project(Document):
    titre: str
    rang: int = 0
    image: Optional[ProjectImage] = None
    categories: List[str] = Field(default_factory=list)
    technos: List[str] = Field(default_factory=list)

    datedebut: Optional[str] = None
    datefin: Optional[str] = None

    soustitre: Optional[str] = None
    chapo: Optional[str] = None
    contenu: Optional[str] = None 

    liens: List[ProjectLink] = Field(default_factory=list)
    images: List[ProjectImage] = Field(default_factory=list)

    class Settings:
        name = "projects"
