from typing import List, Optional

from pydantic import BaseModel, Field
from beanie import PydanticObjectId


class ServiceBase(BaseModel):
    contenu: Optional[str] = None  



class ServiceCreate(BaseModel):
    contenu: Optional[str] = None


class ServiceUpdate(BaseModel):
    contenu: Optional[str] = None


class Service(ServiceBase):
    id: PydanticObjectId

    class Config:
        json_encoders = {PydanticObjectId: str}
