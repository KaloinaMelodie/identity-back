from typing import List, Optional

from pydantic import BaseModel, Field
from beanie import PydanticObjectId


class AwardLinkBase(BaseModel):
    lien: str
    titre: str


class AwardImageIn(BaseModel):
    image: str  # base64 or data url
    alt: str

class AwardImageOut(BaseModel):
    url: str
    key: str
    alt: str

class AwardBase(BaseModel):
    titre: str
    rang: int = 0
    image: Optional[AwardImageOut] = None

    datedebut: Optional[str] = None
    datefin: Optional[str] = None

    chapo: Optional[str] = None
    contenu: Optional[str] = None  

    liens: List[AwardLinkBase] = Field(default_factory=list)
    images: List[AwardImageOut] = Field(default_factory=list)



class AwardCreate(BaseModel):
    titre: str
    rang: int = 0
    image: Optional[AwardImageIn] = None
    datedebut: Optional[str] = None
    datefin: Optional[str] = None
    chapo: Optional[str] = None
    contenu: Optional[str] = None
    liens: List[AwardLinkBase] = Field(default_factory=list)
    images: List[AwardImageIn] = Field(default_factory=list)


class AwardUpdate(BaseModel):
    titre: Optional[str] = None
    rang: Optional[int] = None
    image: Optional[AwardImageIn] = None
    datedebut: Optional[str] = None
    datefin: Optional[str] = None
    chapo: Optional[str] = None
    contenu: Optional[str] = None
    liens: Optional[List[AwardLinkBase]] = None
    images: Optional[List[AwardImageIn]] = None


class AwardOut(AwardBase):
    id: PydanticObjectId

    class Config:
        json_encoders = {PydanticObjectId: str}
