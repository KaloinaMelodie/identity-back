from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status

from schemas.experience import ExperienceCreate, ExperienceUpdate, Experience
from services.experience_service import ExperienceService

router = APIRouter(
    prefix="/experiences",
    tags=["experiences"],
)


@router.post(
    "/",
    response_model=Experience,
    status_code=status.HTTP_201_CREATED,
)
async def create_experience(payload: ExperienceCreate):
    experience = await ExperienceService.create_experience(payload)
    return Experience(**experience.model_dump())


@router.get(
    "/",
    response_model=List[Experience],
)
async def get_experiences():
    experiences = await ExperienceService.list_experiences()
    return [Experience(**p.model_dump()) for p in experiences]


@router.get(
    "/{experience_id}",
    response_model=Experience,
)
async def get_experience(experience_id: PydanticObjectId):
    experience = await ExperienceService.get_experience(experience_id)
    if not experience:
        raise HTTPException(status_code=404, detail="Experience non trouvé")
    return Experience(**experience.model_dump())


@router.put(
    "/{experience_id}",
    response_model=Experience,
)
async def update_experience(experience_id: PydanticObjectId, payload: ExperienceUpdate):
    experience = await ExperienceService.update_experience(experience_id, payload)
    if not experience:
        raise HTTPException(status_code=404, detail="Experience non trouvé")
    return Experience(**experience.model_dump())


@router.delete(
    "/{experience_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_experience(experience_id: PydanticObjectId):
    deleted = await ExperienceService.delete_experience(experience_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Experience non trouvé")
    return None
