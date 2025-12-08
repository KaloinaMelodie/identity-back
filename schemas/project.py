from typing import List, Optional

from pydantic import BaseModel, Field
from beanie import PydanticObjectId


class ProjectLinkBase(BaseModel):
    lien: str
    titre: str


class ProjectImageBase(BaseModel):
    image: str  
    alt: str


class ProjectBase(BaseModel):
    titre: str
    image: Optional[ProjectImageBase] = None
    categories: List[str] = Field(default_factory=list)
    technos: List[str] = Field(default_factory=list)

    datedebut: Optional[str] = None
    datefin: Optional[str] = None

    soustitre: Optional[str] = None
    chapo: Optional[str] = None
    contenu: Optional[str] = None  

    liens: List[ProjectLinkBase] = Field(default_factory=list)
    images: List[ProjectImageBase] = Field(default_factory=list)


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    titre: Optional[str] = None
    image: Optional[ProjectImageBase] = None
    categories: Optional[List[str]] = None
    technos: Optional[List[str]] = None
    datedebut: Optional[str] = None
    datefin: Optional[str] = None
    soustitre: Optional[str] = None
    chapo: Optional[str] = None
    contenu: Optional[str] = None
    liens: Optional[List[ProjectLinkBase]] = None
    images: Optional[List[ProjectImageBase]] = None


class ProjectOut(ProjectBase):
    id: PydanticObjectId

    class Config:
        json_encoders = {PydanticObjectId: str}
