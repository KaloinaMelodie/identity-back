from typing import List, Optional
from beanie import PydanticObjectId

from models.contact import Contact
from schemas.contact import ContactCreate, ContactUpdate
from services.email_service import EmailService
from fastapi import BackgroundTasks

class ContactService:
    @staticmethod
    async def create_contact(
        data: ContactCreate,
        background_tasks: BackgroundTasks
    ) -> Contact:

        contact = Contact(
            name=data.name,
            email=data.email,
            date=data.date,
            contenu=data.contenu
        )

        await contact.insert()
        await contact.save()

        background_tasks.add_task(
            EmailService.send_contact_email,
            data.email,
            data.name,
            data.contenu
        )

        return contact

    @staticmethod
    async def get_contact(contact_id: PydanticObjectId) -> Optional[Contact]:
        return await Contact.get(contact_id)

    @staticmethod
    async def list_contacts() -> List[Contact]:
        return await Contact.find_all().to_list()

    @staticmethod
    async def update_contact(contact_id: PydanticObjectId, data: ContactUpdate) -> Optional[Contact]:
        contact = await Contact.get(contact_id)
        if not contact:
            return None

        update_data = data.model_dump(exclude_unset=True)     

        # Update remaining fields
        for field, value in update_data.items():
            setattr(contact, field, value)

        await contact.save()
        return contact

    @staticmethod
    async def delete_contact(contact_id: PydanticObjectId) -> bool:
        contact = await Contact.get(contact_id)
        if not contact:
            return False     

        await contact.delete()
        return True
