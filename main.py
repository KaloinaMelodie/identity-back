from fastapi import FastAPI
from core.database import initiate_database
from routers import include_routes
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

MEDIA_ROOT = os.getenv("MEDIA_ROOT", "media")
MEDIA_URL = os.getenv("MEDIA_URL", "/api/media")

app.mount(MEDIA_URL, StaticFiles(directory=MEDIA_ROOT), name="media")

origins = [
    "http://localhost:5173",
    "http://localhost:4173",
    "https://front-identity.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],     # GET, POST, PUT, DELETE…
    allow_headers=["*"],     # tous les headers
)

@app.middleware("http")
async def force_https(request, call_next):
    response = await call_next(request)
    # Ne pas rediriger vers HTTP
    return response

@app.on_event("startup")
async def start_db():
    await initiate_database()
    print("")


include_routes(app) 

@app.get("/")
def read_root():
    return {"Hello": "World"}
