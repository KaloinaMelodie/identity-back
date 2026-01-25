from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from services.cv_service import cv_service
import logging

router = APIRouter(
    prefix="/cv",
    tags=["CV Management"]
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@router.post("/upload")
async def upload_cv(file: UploadFile = File(...)):
    return await cv_service.create_cv(file)


@router.get("/info")
async def get_cv_info():
    return cv_service.get_cv_info()


@router.get("/exists")
async def check_cv_exists():
    return {
        "exists": cv_service.cv_exists()
    }


@router.get("/download")
async def download_cv():
    cv_path = cv_service.get_cv()
    
    return FileResponse(
        path=cv_path,
        filename=f"CV_{cv_path.stem}.pdf",  
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=CV.pdf"
        }
    )


@router.put("/update")
async def update_cv(file: UploadFile = File(...)):
    return await cv_service.update_cv(file)


@router.delete("/delete")
async def delete_cv():
    return cv_service.delete_cv()