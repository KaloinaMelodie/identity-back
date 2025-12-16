from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status

from schemas.service import ServiceCreate, ServiceUpdate, Service
from services.service_service import ServiceService

router = APIRouter(
    prefix="/services",
    tags=["services"],
)


@router.post(
    "/",
    response_model=Service,
    status_code=status.HTTP_201_CREATED,
)
async def create_service(payload: ServiceCreate):
    service = await ServiceService.create_service(payload)
    return Service(**service.model_dump())


@router.get(
    "/",
    response_model=List[Service],
)
async def get_services():
    services = await ServiceService.list_services()
    return [Service(**p.model_dump()) for p in services]


@router.get(
    "/{service_id}",
    response_model=Service,
)
async def get_service(service_id: PydanticObjectId):
    service = await ServiceService.get_service(service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Projet non trouvé")
    return Service(**service.model_dump())


@router.put(
    "/{service_id}",
    response_model=Service,
)
async def update_service(service_id: PydanticObjectId, payload: ServiceUpdate):
    service = await ServiceService.update_service(service_id, payload)
    if not service:
        raise HTTPException(status_code=404, detail="Projet non trouvé")
    return Service(**service.model_dump())


@router.delete(
    "/{service_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_service(service_id: PydanticObjectId):
    deleted = await ServiceService.delete_service(service_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Projet non trouvé")
    return None
