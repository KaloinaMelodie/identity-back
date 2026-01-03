from typing import List, Optional
from beanie import PydanticObjectId
from typing import Dict, List, Tuple
from collections import defaultdict

from models.techno import Techno, TechnoImage
from schemas.techno import TechnoCreate, TechnoImageOut, TechnoUpdate
from schemas.techno_grouped import TechnoGroupOut, TechnoItemOut
from services.media_storage import save_techno_image, delete_media_key

class TechnoService:
    @staticmethod
    async def create_techno(data: TechnoCreate) -> Techno:
        # Create techno first to get id
        techno = Techno(
            titre=data.titre,          
            chapo=data.chapo, 
            categorie=data.categorie,         
            image=None,
        )
        await techno.insert()

        # Save main image
        if data.image and data.image.image:
            url, key = save_techno_image(str(techno.id), data.image.image)
            techno.image = TechnoImage(url=url, key=key, alt=data.image.alt)
      

        await techno.save()
        return techno

    @staticmethod
    async def list_technos_grouped(chunk_size: int = 4) -> List[TechnoGroupOut]:
        technos = await Techno.find_all().to_list()

        # key: categorie normalisée (case-insensitive)
        grouped: Dict[str, List[Techno]] = defaultdict(list)
        display_name: Dict[str, str] = {}

        for t in technos:
            raw = (t.categorie or "").strip()
            key = raw.casefold()  # mieux que lower() pour unicode
            if key not in display_name:
                display_name[key] = (raw.title() if raw else "Autre")
            grouped[key].append(t)

        result: List[TechnoGroupOut] = []

        def to_image_out(img):
            if not img:
                return None
            return TechnoImageOut(url=img.url, key=img.key, alt=img.alt)

        # optionnel: trier par categorie
        for cat_key in sorted(grouped.keys(), key=lambda x: display_name[x].casefold()):
            items = grouped[cat_key]

            # optionnel: trier les technos dans la categorie (par titre)
            items.sort(key=lambda x: (x.titre or "").casefold())

            # chunk par 4
            for i in range(0, len(items), chunk_size):
                chunk = items[i:i + chunk_size]

                result.append(
                    TechnoGroupOut(
                        categorie=display_name[cat_key],
                        technos=[
                            TechnoItemOut(
                                titre=c.titre,
                                chapo=c.chapo,
                                image=to_image_out(c.image).model_dump() if c.image else None

                            )
                            for c in chunk
                        ],
                    )
                )

        return result

    @staticmethod
    async def get_techno(techno_id: PydanticObjectId) -> Optional[Techno]:
        return await Techno.get(techno_id)

    @staticmethod
    async def list_technos() -> List[Techno]:
        return await Techno.find_all().to_list()

    @staticmethod
    async def update_techno(techno_id: PydanticObjectId, data: TechnoUpdate) -> Optional[Techno]:
        techno = await Techno.get(techno_id)
        if not techno:
            return None

        update_data = data.model_dump(exclude_unset=True)

        # If main image provided: delete old + save new
        if "image" in update_data and update_data["image"] is not None:
            new_img = update_data["image"]
            if techno.image:
                delete_media_key(techno.image.key)
            url, key = save_techno_image(str(techno.id), new_img["image"])
            techno.image = TechnoImage(url=url, key=key, alt=new_img.get("alt", ""))

            # remove from normal setattr loop
            update_data.pop("image", None)


        # Update remaining fields
        for field, value in update_data.items():
            setattr(techno, field, value)

        await techno.save()
        return techno

    @staticmethod
    async def delete_techno(techno_id: PydanticObjectId) -> bool:
        techno = await Techno.get(techno_id)
        if not techno:
            return False

        # delete media files
        if techno.image:
            delete_media_key(techno.image.key)

        await techno.delete()
        return True
