from fastapi import FastAPI
from routers.project_route import router as  projectRoute
from routers.auth_route import router as  authRoute
from routers.service_route import router as  serviceRoute
from routers.techno_route import router as  technoRoute
from routers.experience_route import router as  experienceRoute
from routers.award_route import router as  awardRoute
from routers.cv_route import router as  cvRoute
from routers.contact_route import router as  contactRoute
ROUTERS = [
    projectRoute,
    authRoute,
    serviceRoute,
    technoRoute,
    experienceRoute,
    awardRoute,
    cvRoute,
    contactRoute,
]

def include_routes(app: FastAPI, api_prefix: str = "/api"):
    for router in ROUTERS:
        app.include_router(router, prefix=api_prefix)
