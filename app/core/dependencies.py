from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.quests.repository import QuestionnaireRepository
from app.quests.use_case import QuestionnaireUseCase


def get_use_case(session: AsyncSession = Depends(get_session)) -> QuestionnaireUseCase:
    return QuestionnaireUseCase(QuestionnaireRepository(session))