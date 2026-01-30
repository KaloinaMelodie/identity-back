from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status,BackgroundTasks

from schemas.contact import ContactCreate, ContactUpdate, Contact
from services.contact_service import ContactService

router = APIRouter(
    prefix="/contacts",
    tags=["contacts"],
)


@router.post(
    "/",
    response_model=Contact,
    status_code=status.HTTP_201_CREATED,
    
)
async def create_contact(payload: ContactCreate,background_tasks: BackgroundTasks):
    contact = await ContactService.create_contact(payload, background_tasks)
    return Contact(**contact.model_dump())


@router.get(
    "/",
    response_model=List[Contact],
)
async def get_contacts():
    contacts = await ContactService.list_contacts()
    return [Contact(**p.model_dump()) for p in contacts]


@router.get(
    "/{contact_id}",
    response_model=Contact,
)
async def get_contact(contact_id: PydanticObjectId):
    contact = await ContactService.get_contact(contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact non trouvé")
    return Contact(**contact.model_dump())


@router.put(
    "/{contact_id}",
    response_model=Contact,
)
async def update_contact(contact_id: PydanticObjectId, payload: ContactUpdate):
    contact = await ContactService.update_contact(contact_id, payload)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact non trouvé")
    return Contact(**contact.model_dump())


@router.delete(
    "/{contact_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_contact(contact_id: PydanticObjectId):
    deleted = await ContactService.delete_contact(contact_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Contact non trouvé")
    return None
