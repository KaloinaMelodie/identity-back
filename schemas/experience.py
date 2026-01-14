from typing import List, Optional

from pydantic import BaseModel, Field
from beanie import PydanticObjectId


class ExperienceLinkBase(BaseModel):
    lien: str
    titre: str


class ExperienceBase(BaseModel):
    titre: str
    rang: int = 0
    organisation: Optional[str] = None

    datedebut: Optional[str] = None
    datefin: Optional[str] = None

    chapo: Optional[str] = None
    contenu: Optional[str] = None  

    liens: List[ExperienceLinkBase] = Field(default_factory=list)



class ExperienceCreate(BaseModel):
    titre: str
    rang: int = 0
    organisation: Optional[str] = None

    datedebut: Optional[str] = None
    datefin: Optional[str] = None

    chapo: Optional[str] = None
    contenu: Optional[str] = None
    liens: List[ExperienceLinkBase] = Field(default_factory=list)


class ExperienceUpdate(BaseModel):
    titre: Optional[str] = None
    rang: Optional[int] = None
    organisation: Optional[str] = None
    datedebut: Optional[str] = None
    datefin: Optional[str] = None
    chapo: Optional[str] = None
    contenu: Optional[str] = None
    liens: Optional[List[ExperienceLinkBase]] = None


class Experience(ExperienceBase):
    id: PydanticObjectId

    class Config:
        json_encoders = {PydanticObjectId: str}
