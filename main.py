from fastapi import FastAPI, Request 
from core.database import initiate_database
from routers import include_routes
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

    
app = FastAPI()

MEDIA_ROOT = os.getenv("MEDIA_ROOT", "media")
MEDIA_URL = os.getenv("MEDIA_URL", "/api/media")

class CacheControlMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if request.url.path.startswith(MEDIA_URL):
            response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        return response

app.add_middleware(CacheControlMiddleware) 
app.mount(MEDIA_URL, StaticFiles(directory=MEDIA_ROOT), name="media")

origins = [
    "http://localhost:5173",
    "http://localhost:4173",
    "https://front-identity.onrender.com",
    "http://localhost:4200",
    "https://kaloina-melodie-860478262732.europe-west1.run.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],     # GET, POST, PUT, DELETE…
    allow_headers=["*"],     # tous les headers
)


@app.on_event("startup")
async def start_db():
    await initiate_database()
    print("")


include_routes(app) 

@app.head("/")
@app.get("/")
async def root():
    return {"message": "Service is running"}