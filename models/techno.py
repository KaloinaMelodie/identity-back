from typing import List, Optional

from beanie import Document
from pydantic import BaseModel, Field



class TechnoImage(BaseModel):
    url: str
    key: str
    alt: str


class Techno(Document):
    titre: str
    categorie: str
    image: Optional[TechnoImage] = None   
    chapo: Optional[str] = None
   
    class Settings:
        name = "technos"
