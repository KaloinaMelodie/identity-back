from typing import List, Optional
from pydantic import BaseModel


class TechnoImageOut(BaseModel):
    url: str
    key: str
    alt: str


class TechnoItemOut(BaseModel):
    titre: str
    chapo: Optional[str] = None
    image: Optional[TechnoImageOut] = None


class TechnoGroupOut(BaseModel):
    categorie: str
    technos: List[TechnoItemOut]
