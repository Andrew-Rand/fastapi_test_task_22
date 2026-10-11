from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db import SessionFactory, engine, get_session
from app.repository import QuestionnaireRepository
from app.schemas import ErrorResponse, QuestionnaireDetail, QuestionnaireShort
from app.seed import seed_data
from app.use_case import QuestionnaireNotFound, QuestionnaireUseCase


@asynccontextmanager
async def lifespan(_: FastAPI):
    # TODO: handle errors to start app if seed not working
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


# TODO: move to dependencies
# TODO: rewrite as a type
def get_use_case(session: AsyncSession = Depends(get_session)) -> QuestionnaireUseCase:
    return QuestionnaireUseCase(QuestionnaireRepository(session))


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get(
    "/api/v1/questionnaires",
    response_model=list[QuestionnaireShort],
    summary="Available questionnaires",
)
async def list_questionnaires(
    service: QuestionnaireUseCase = Depends(get_use_case),
) -> list[QuestionnaireShort]:
    return await service.get_list()


@app.get(
    "/api/v1/questionnaires/{cod}",
    response_model=QuestionnaireDetail,
    responses={404: {"model": ErrorResponse}},
    summary="Get questionnaire template",
)
async def get_questionnaire(
    cod: int,
    service: QuestionnaireUseCase = Depends(get_use_case),
) -> QuestionnaireDetail:
    try:
        return await service.get_item(cod)
    except QuestionnaireNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Questionnaire not found or unavailable",
        ) from None