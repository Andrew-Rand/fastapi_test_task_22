from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from app.core.dependencies import get_use_case
from app.core.schemas import BaseErrorResponse
from app.quests.schemas import QuestionnaireShort, QuestionnaireDetail
from app.quests.use_case import QuestionnaireUseCase, QuestionnaireNotFound

router = APIRouter(prefix="/api/v1")

@router.get(path="/questionnaires", response_model=list[QuestionnaireShort], summary="Available questionnaires")
async def list_questionnaires(
    service: QuestionnaireUseCase = Depends(get_use_case),
) -> list[QuestionnaireShort]:
    return await service.get_list()


@router.get(
    path="/questionnaires/{cod}",
    response_model=QuestionnaireDetail,
    responses={404: {"model": BaseErrorResponse}},
    summary="Get questionnaire template",
)
async def get_questionnaire(cod: int, service: QuestionnaireUseCase = Depends(get_use_case)) -> QuestionnaireDetail:
    try:
        return await service.get_item(cod)
    except QuestionnaireNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Questionnaire not found or unavailable")