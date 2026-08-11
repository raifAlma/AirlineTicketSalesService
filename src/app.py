from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.api_v1 import router as api_v1_router
from container import Container
from settings import settings

container = Container()

@asynccontextmanager
async def lifespan(app: FastAPI):
    sessionmanager = container.session_manager()
    sessionmanager.init(settings.database.get_database_url())
    print(f"Connecting to database with URL: {settings.database.get_database_url()}")
    try:
        yield
    finally:
        await sessionmanager.close()

container.wire(modules=["infrastructure.database.postgresql.session"])

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router)