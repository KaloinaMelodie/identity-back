from typing import List, Optional
from beanie import PydanticObjectId

from models.service import Service
from schemas.service import ServiceCreate, ServiceUpdate

class ServiceService:
    @staticmethod
    async def create_service(data: ServiceCreate) -> Service:
        # Create service first to get id
        service = Service(
            contenu=data.contenu,
        )
        await service.insert()

        await service.save()
        return service

    @staticmethod
    async def get_service(service_id: PydanticObjectId) -> Optional[Service]:
        return await Service.get(service_id)

    @staticmethod
    async def list_services() -> List[Service]:
        return await Service.find_all().to_list()

    @staticmethod
    async def update_service(service_id: PydanticObjectId, data: ServiceUpdate) -> Optional[Service]:
        service = await Service.get(service_id)
        if not service:
            return None

        update_data = data.model_dump(exclude_unset=True)
        # Update remaining fields
        for field, value in update_data.items():
            setattr(service, field, value)

        await service.save()
        return service

    @staticmethod
    async def delete_service(service_id: PydanticObjectId) -> bool:
        service = await Service.get(service_id)
        if not service:
            return False

        await service.delete()
        return True
