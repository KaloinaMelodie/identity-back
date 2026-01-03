from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status

from schemas.project import ProjectCreate, ProjectUpdate, ProjectOut
from services.project_service import ProjectService

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


@router.post(
    "/",
    response_model=ProjectOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(payload: ProjectCreate):
    project = await ProjectService.create_project(payload)
    return ProjectOut(**project.model_dump())


@router.get(
    "/",
    response_model=List[ProjectOut],
)
async def get_projects():
    projects = await ProjectService.list_projects()
    return [ProjectOut(**p.model_dump()) for p in projects]


@router.get(
    "/{project_id}",
    response_model=ProjectOut,
)
async def get_project(project_id: PydanticObjectId):
    project = await ProjectService.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Projet non trouvé")
    return ProjectOut(**project.model_dump())


@router.put(
    "/{project_id}",
    response_model=ProjectOut,
)
async def update_project(project_id: PydanticObjectId, payload: ProjectUpdate):
    project = await ProjectService.update_project(project_id, payload)
    if not project:
        raise HTTPException(status_code=404, detail="Projet non trouvé")
    return ProjectOut(**project.model_dump())


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project(project_id: PydanticObjectId):
    deleted = await ProjectService.delete_project(project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Projet non trouvé")
    return None
