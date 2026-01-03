from typing import List, Optional
from beanie import PydanticObjectId

from models.project import Project, ProjectImage, ProjectLink
from schemas.project import ProjectCreate, ProjectUpdate
from services.media_storage import save_project_image, delete_media_key

class ProjectService:
    @staticmethod
    async def create_project(data: ProjectCreate) -> Project:
        # Create project first to get id
        project = Project(
            titre=data.titre,
            rang=data.rang,
            categories=data.categories,
            technos=data.technos,
            datedebut=data.datedebut,
            datefin=data.datefin,
            soustitre=data.soustitre,
            chapo=data.chapo,
            contenu=data.contenu,
            liens=[ProjectLink(**l.model_dump()) for l in data.liens],
            images=[],
            image=None,
        )
        await project.insert()

        # Save main image
        if data.image and data.image.image:
            url, key = save_project_image(str(project.id), data.image.image)
            project.image = ProjectImage(url=url, key=key, alt=data.image.alt)

        # Save gallery
        if data.images:
            gallery: List[ProjectImage] = []
            for img in data.images:
                url, key = save_project_image(str(project.id), img.image)
                gallery.append(ProjectImage(url=url, key=key, alt=img.alt))
            project.images = gallery

        await project.save()
        return project

    @staticmethod
    async def get_project(project_id: PydanticObjectId) -> Optional[Project]:
        return await Project.get(project_id)

    @staticmethod
    async def list_projects() -> List[Project]:
        return await Project.find_all().to_list()

    @staticmethod
    async def update_project(project_id: PydanticObjectId, data: ProjectUpdate) -> Optional[Project]:
        project = await Project.get(project_id)
        if not project:
            return None

        update_data = data.model_dump(exclude_unset=True)

        # If main image provided: delete old + save new
        if "image" in update_data and update_data["image"] is not None:
            new_img = update_data["image"]
            if project.image:
                delete_media_key(project.image.key)
            url, key = save_project_image(str(project.id), new_img["image"])
            project.image = ProjectImage(url=url, key=key, alt=new_img.get("alt", ""))

            # remove from normal setattr loop
            update_data.pop("image", None)

        # If gallery provided: replace all (delete old + save new)
        if "images" in update_data and update_data["images"] is not None:
            # delete old
            for old in project.images or []:
                delete_media_key(old.key)

            new_gallery: List[ProjectImage] = []
            for img in update_data["images"]:
                url, key = save_project_image(str(project.id), img["image"])
                new_gallery.append(ProjectImage(url=url, key=key, alt=img.get("alt", "")))
            project.images = new_gallery

            update_data.pop("images", None)

        # Update remaining fields
        for field, value in update_data.items():
            setattr(project, field, value)

        await project.save()
        return project

    @staticmethod
    async def delete_project(project_id: PydanticObjectId) -> bool:
        project = await Project.get(project_id)
        if not project:
            return False

        # delete media files
        if project.image:
            delete_media_key(project.image.key)
        for img in project.images or []:
            delete_media_key(img.key)

        await project.delete()
        return True
