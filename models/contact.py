from typing import List, Optional

from beanie import Document
from pydantic import BaseModel, Field



class Contact(Document):
    name: str
    email: Optional[str] = None

    date: Optional[str] = None
    contenu: Optional[str] = None 


    class Settings:
        name = "contacts"
