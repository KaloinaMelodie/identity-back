from typing import List, Optional

from pydantic import BaseModel, Field
from beanie import PydanticObjectId


class ProjectLinkBase(BaseModel):
    lien: str
    titre: str


class ProjectImageIn(BaseModel):
    image: str  # base64 or data url
    alt: str

class ProjectImageOut(BaseModel):
    url: str
    key: str
    alt: str

class ProjectBase(BaseModel):
    titre: str
    rang: int = 0
    image: Optional[ProjectImageOut] = None
    categories: List[str] = Field(default_factory=list)
    technos: List[str] = Field(default_factory=list)

    datedebut: Optional[str] = None
    datefin: Optional[str] = None

    soustitre: Optional[str] = None
    chapo: Optional[str] = None
    contenu: Optional[str] = None  

    liens: List[ProjectLinkBase] = Field(default_factory=list)
    images: List[ProjectImageOut] = Field(default_factory=list)



class ProjectCreate(BaseModel):
    titre: str
    rang: int = 0
    image: Optional[ProjectImageIn] = None
    categories: List[str] = Field(default_factory=list)
    technos: List[str] = Field(default_factory=list)
    datedebut: Optional[str] = None
    datefin: Optional[str] = None
    soustitre: Optional[str] = None
    chapo: Optional[str] = None
    contenu: Optional[str] = None
    liens: List[ProjectLinkBase] = Field(default_factory=list)
    images: List[ProjectImageIn] = Field(default_factory=list)


class ProjectUpdate(BaseModel):
    titre: Optional[str] = None
    rang: Optional[int] = None
    image: Optional[ProjectImageIn] = None
    categories: Optional[List[str]] = None
    technos: Optional[List[str]] = None
    datedebut: Optional[str] = None
    datefin: Optional[str] = None
    soustitre: Optional[str] = None
    chapo: Optional[str] = None
    contenu: Optional[str] = None
    liens: Optional[List[ProjectLinkBase]] = None
    images: Optional[List[ProjectImageIn]] = None


class ProjectOut(ProjectBase):
    id: PydanticObjectId

    class Config:
        json_encoders = {PydanticObjectId: str}
