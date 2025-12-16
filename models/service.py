from typing import List, Optional

from beanie import Document
from pydantic import BaseModel, Field



class Service(Document):
    contenu: Optional[str] = None 

    class Settings:
        name = "services"
