from pathlib import Path
from typing import Optional
from fastapi import UploadFile, HTTPException
from datetime import datetime
import shutil
import os

class CVService:
    def __init__(self, cv_directory: str = "media/cv"):
        self.cv_directory = Path(cv_directory)
        self.cv_directory.mkdir(parents=True, exist_ok=True)
        self.allowed_extensions = {'.pdf', '.doc', '.docx'}
    
    def _get_current_cv_path(self) -> Optional[Path]:
        cv_files = list(self.cv_directory.glob("*"))
        cv_files = [f for f in cv_files if f.suffix.lower() in self.allowed_extensions]
        
        if cv_files:
            return max(cv_files, key=lambda f: f.stat().st_mtime)
        return None
    
    def _validate_file(self, file: UploadFile) -> None:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in self.allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed types: {', '.join(self.allowed_extensions)}"
            )
    
    def _delete_old_cvs(self) -> None:
        for cv_file in self.cv_directory.glob("*"):
            if cv_file.suffix.lower() in self.allowed_extensions:
                cv_file.unlink()
    
    async def create_cv(self, file: UploadFile) -> dict:
        self._validate_file(file)
        
        self._delete_old_cvs()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_ext = Path(file.filename).suffix.lower()
        new_filename = f"cv_{timestamp}{file_ext}"
        file_path = self.cv_directory / new_filename
        
        try:
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
        finally:
            await file.close()
        
        return {
            "message": "CV uploaded successfully",
            "filename": new_filename,
            "size": file_path.stat().st_size,
            "uploaded_at": datetime.now().isoformat()
        }
    
    def get_cv(self) -> Path:
        cv_path = self._get_current_cv_path()
        
        if not cv_path or not cv_path.exists():
            raise HTTPException(status_code=404, detail="CV not found")
        
        return cv_path
    
    def get_cv_info(self) -> dict:
        cv_path = self._get_current_cv_path()
        
        if not cv_path or not cv_path.exists():
            raise HTTPException(status_code=404, detail="CV not found")
        
        stat = cv_path.stat()
        return {
            "filename": cv_path.name,
            "size": stat.st_size,
            "size_mb": round(stat.st_size / (1024 * 1024), 2),
            "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "extension": cv_path.suffix
        }
    
    async def update_cv(self, file: UploadFile) -> dict:
        return await self.create_cv(file)
    
    def delete_cv(self) -> dict:
        cv_path = self._get_current_cv_path()
        
        if not cv_path or not cv_path.exists():
            raise HTTPException(status_code=404, detail="CV not found")
        
        filename = cv_path.name
        cv_path.unlink()
        
        return {
            "message": "CV deleted successfully",
            "deleted_filename": filename,
            "deleted_at": datetime.now().isoformat()
        }
    
    def cv_exists(self) -> bool:
        """Check if a CV exists"""
        cv_path = self._get_current_cv_path()
        return cv_path is not None and cv_path.exists()


cv_service = CVService()