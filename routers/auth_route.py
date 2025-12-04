from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models.user import User
from services.utils import hash_password, verify_password, create_access_token
from pydantic import BaseModel
import logging

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Utilisateur non trouvé erico"}}
    )

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RegisterModel(BaseModel):
    email: str
    full_name: str
    password: str

@router.post("/register")
async def register_user(user: RegisterModel):
    existing = await User.find_one(User.email == user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email déjà enregistré")
    logging.info(user.password)
    logging.info(len(user.password.encode()))
    hashed_pw = hash_password(user.password)
    new_user = User(email=user.email, full_name=user.full_name, password=user.password,hashed_password=hashed_pw)
    await new_user.insert()
    return {"message": "Utilisateur créé avec succès"}


class LoginModel(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login_json(payload: LoginModel):
    user = await User.find_one(User.email == payload.email)
    if not user:
        raise HTTPException(status_code=401, detail="Utilisateur non trouvé")
    if hasattr(user, "hashed_password"):
        if not verify_password(payload.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Mot de passe incorrect")
    else:
        if user.password != payload.password:
            raise HTTPException(status_code=401, detail="Mot de passe incorrect")

    token = create_access_token({"sub": user.email})
    return {"name":user.full_name,"access_token": token, "token_type": "bearer"}
