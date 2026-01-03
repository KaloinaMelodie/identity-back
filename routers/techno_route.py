from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status

from schemas.techno import TechnoCreate, TechnoUpdate, Techno
from schemas.techno_grouped import TechnoGroupOut
from services.techno_service import TechnoService

router = APIRouter(
    prefix="/technos",
    tags=["technos"],
)

@router.get("/grouped", response_model=List[TechnoGroupOut])
async def get_technos_grouped():
    return await TechnoService.list_technos_grouped(chunk_size=4)

@router.post(
    "/",
    response_model=Techno,
    status_code=status.HTTP_201_CREATED,
)
async def create_techno(payload: TechnoCreate):
    techno = await TechnoService.create_techno(payload)
    return Techno(**techno.model_dump())


@router.get(
    "/",
    response_model=List[Techno],
)
async def get_technos():
    technos = await TechnoService.list_technos()
    return [Techno(**p.model_dump()) for p in technos]


@router.get(
    "/{techno_id}",
    response_model=Techno,
)
async def get_techno(techno_id: PydanticObjectId):
    techno = await TechnoService.get_techno(techno_id)
    if not techno:
        raise HTTPException(status_code=404, detail="Techno non trouvé")
    return Techno(**techno.model_dump())


@router.put(
    "/{techno_id}",
    response_model=Techno,
)
async def update_techno(techno_id: PydanticObjectId, payload: TechnoUpdate):
    techno = await TechnoService.update_techno(techno_id, payload)
    if not techno:
        raise HTTPException(status_code=404, detail="Techno non trouvé")
    return Techno(**techno.model_dump())


@router.delete(
    "/{techno_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_techno(techno_id: PydanticObjectId):
    deleted = await TechnoService.delete_techno(techno_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Techno non trouvé")
    return None
