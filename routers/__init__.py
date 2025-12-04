from fastapi import FastAPI
from routers.project_route import router as  projectRoute
from routers.auth_route import router as  authRoute

ROUTERS = [
    projectRoute,
    authRoute
]

def include_routes(app: FastAPI, api_prefix: str = "/api"):
    for router in ROUTERS:
        app.include_router(router, prefix=api_prefix)
