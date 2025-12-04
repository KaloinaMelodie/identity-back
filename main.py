from fastapi import FastAPI
from core.database import initiate_database
from routers import include_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:4173",
    "https://front-matching.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],     # GET, POST, PUT, DELETE…
    allow_headers=["*"],     # tous les headers
)

@app.on_event("startup")
async def start_db():
    await initiate_database()
    print("")


include_routes(app) 

@app.get("/")
def read_root():
    return {"Hello": "World"}
