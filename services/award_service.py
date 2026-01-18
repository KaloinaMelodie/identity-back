from typing import List, Optional
from beanie import PydanticObjectId

from models.award import Award, AwardImage, AwardLink
from schemas.award import AwardCreate, AwardUpdate
from services.media_storage import save_award_image, delete_media_key

class AwardService:
    @staticmethod
    async def create_award(data: AwardCreate) -> Award:
        # Create award first to get id
        award = Award(
            titre=data.titre,
            rang=data.rang,            
            datedebut=data.datedebut,
            datefin=data.datefin,
            chapo=data.chapo,
            contenu=data.contenu,
            liens=[AwardLink(**l.model_dump()) for l in data.liens],
            images=[],
            image=None,
        )
        await award.insert()

        # Save main image
        if data.image and data.image.image:
            url, key = save_award_image(str(award.id), data.image.image)
            award.image = AwardImage(url=url, key=key, alt=data.image.alt)

        # Save gallery
        if data.images:
            gallery: List[AwardImage] = []
            for img in data.images:
                url, key = save_award_image(str(award.id), img.image)
                gallery.append(AwardImage(url=url, key=key, alt=img.alt))
            award.images = gallery

        await award.save()
        return award

    @staticmethod
    async def get_award(award_id: PydanticObjectId) -> Optional[Award]:
        return await Award.get(award_id)

    @staticmethod
    async def list_awards() -> List[Award]:
        return await Award.find_all().to_list()

    @staticmethod
    async def update_award(award_id: PydanticObjectId, data: AwardUpdate) -> Optional[Award]:
        award = await Award.get(award_id)
        if not award:
            return None

        update_data = data.model_dump(exclude_unset=True)

        # If main image provided: delete old + save new
        if "image" in update_data and update_data["image"] is not None:
            new_img = update_data["image"]
            if award.image:
                delete_media_key(award.image.key)
            url, key = save_award_image(str(award.id), new_img["image"])
            award.image = AwardImage(url=url, key=key, alt=new_img.get("alt", ""))

            # remove from normal setattr loop
            update_data.pop("image", None)

        # If gallery provided: replace all (delete old + save new)
        if "images" in update_data and update_data["images"] is not None:
            # delete old
            for old in award.images or []:
                delete_media_key(old.key)

            new_gallery: List[AwardImage] = []
            for img in update_data["images"]:
                url, key = save_award_image(str(award.id), img["image"])
                new_gallery.append(AwardImage(url=url, key=key, alt=img.get("alt", "")))
            award.images = new_gallery

            update_data.pop("images", None)

        # Update remaining fields
        for field, value in update_data.items():
            setattr(award, field, value)

        await award.save()
        return award

    @staticmethod
    async def delete_award(award_id: PydanticObjectId) -> bool:
        award = await Award.get(award_id)
        if not award:
            return False

        # delete media files
        if award.image:
            delete_media_key(award.image.key)
        for img in award.images or []:
            delete_media_key(img.key)

        await award.delete()
        return True
