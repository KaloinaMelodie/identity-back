from typing import List, Optional

from beanie import PydanticObjectId

from models.project import Project
from schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    @staticmethod
    async def create_project(data: ProjectCreate) -> Project:
        project = Project(**data.model_dump())
        await project.insert()
        return project

    @staticmethod
    async def get_project(project_id: PydanticObjectId) -> Optional[Project]:
        return await Project.get(project_id)

    @staticmethod
    async def list_projects() -> List[Project]:
        return await Project.find_all().to_list()

    @staticmethod
    async def update_project(
        project_id: PydanticObjectId,
        data: ProjectUpdate,
    ) -> Optional[Project]:
        project = await Project.get(project_id)
        if not project:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(project, field, value)

        await project.save()
        return project

    @staticmethod
    async def delete_project(project_id: PydanticObjectId) -> bool:
        project = await Project.get(project_id)
        if not project:
            return False

        await project.delete()
        return True
