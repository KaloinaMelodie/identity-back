from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status

from schemas.award import AwardCreate, AwardUpdate, AwardOut
from services.award_service import AwardService

router = APIRouter(
    prefix="/awards",
    tags=["awards"],
)


@router.post(
    "/",
    response_model=AwardOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_award(payload: AwardCreate):
    award = await AwardService.create_award(payload)
    return AwardOut(**award.model_dump())


@router.get(
    "/",
    response_model=List[AwardOut],
)
async def get_awards():
    awards = await AwardService.list_awards()
    return [AwardOut(**p.model_dump()) for p in awards]


@router.get(
    "/{award_id}",
    response_model=AwardOut,
)
async def get_award(award_id: PydanticObjectId):
    award = await AwardService.get_award(award_id)
    if not award:
        raise HTTPException(status_code=404, detail="Award non trouvé")
    return AwardOut(**award.model_dump())


@router.put(
    "/{award_id}",
    response_model=AwardOut,
)
async def update_award(award_id: PydanticObjectId, payload: AwardUpdate):
    award = await AwardService.update_award(award_id, payload)
    if not award:
        raise HTTPException(status_code=404, detail="Award non trouvé")
    return AwardOut(**award.model_dump())


@router.delete(
    "/{award_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_award(award_id: PydanticObjectId):
    deleted = await AwardService.delete_award(award_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Award non trouvé")
    return None
