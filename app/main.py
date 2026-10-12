from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.core.db import SessionFactory, engine
from app.seed import seed_data
from app.quests.router import router as quests_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    # TODO: handle errors and send alert to start app if seed not working
    async with SessionFactory() as session:
        await seed_data(session, settings.data_dir)
    yield
    await engine.dispose()


app = FastAPI(
    title="Medical Templates API",
    description="",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(router=quests_router)
