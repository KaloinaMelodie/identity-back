from fastapi import FastAPI
from routers.project_route import router as  projectRoute
from routers.auth_route import router as  authRoute
from routers.service_route import router as  serviceRoute
from routers.techno_route import router as  technoRoute
ROUTERS = [
    projectRoute,
    authRoute,
    serviceRoute,
    technoRoute,
]

def include_routes(app: FastAPI, api_prefix: str = "/api"):
    for router in ROUTERS:
        app.include_router(router, prefix=api_prefix)
