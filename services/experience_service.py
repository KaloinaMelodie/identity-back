from typing import List, Optional
from beanie import PydanticObjectId

from models.experience import Experience, ExperienceLink
from schemas.experience import ExperienceCreate, ExperienceUpdate

class ExperienceService:
    @staticmethod
    async def create_experience(data: ExperienceCreate) -> Experience:
        # Create experience first to get id
        experience = Experience(
            titre=data.titre,
            rang=data.rang,
            organisation=data.organisation,
            datedebut=data.datedebut,
            datefin=data.datefin,
            chapo=data.chapo,
            contenu=data.contenu,
            liens=[ExperienceLink(**l.model_dump()) for l in data.liens]
        )
        await experience.insert()
       
        await experience.save()
        return experience

    @staticmethod
    async def get_experience(experience_id: PydanticObjectId) -> Optional[Experience]:
        return await Experience.get(experience_id)

    @staticmethod
    async def list_experiences() -> List[Experience]:
        return await Experience.find_all().to_list()

    @staticmethod
    async def update_experience(experience_id: PydanticObjectId, data: ExperienceUpdate) -> Optional[Experience]:
        experience = await Experience.get(experience_id)
        if not experience:
            return None

        update_data = data.model_dump(exclude_unset=True)     

        # Update remaining fields
        for field, value in update_data.items():
            setattr(experience, field, value)

        await experience.save()
        return experience

    @staticmethod
    async def delete_experience(experience_id: PydanticObjectId) -> bool:
        experience = await Experience.get(experience_id)
        if not experience:
            return False     

        await experience.delete()
        return True
