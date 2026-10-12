from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.quests.const import (
    QUESTIONNAIRE_IDENT_MARK,
    ANSWER_IDENT_SHIFT,
    QUESTION_GROUP_IDENT_MARK,
    QUESTION_CODE,
    QUESTION_COUNT_4_MARK,
)
from app.quests.models import Question, ReferenceItem


class QuestionnaireRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_available(self) -> list[ReferenceItem]:
        stmt = (
            select(ReferenceItem)
            .where(
                ReferenceItem.ident == QUESTIONNAIRE_IDENT_MARK,
                or_(ReferenceItem.tip2 == 0, ReferenceItem.tip2.is_(None)),
                ReferenceItem.flag_deleted.is_(False),
            )
            .order_by(ReferenceItem.name.asc().nulls_last())
        )
        return list((await self.session.scalars(stmt)).all())

    async def get_questionnaire(self, cod: int) -> ReferenceItem | None:
        stmt = select(ReferenceItem).where(
            ReferenceItem.ident == QUESTIONNAIRE_IDENT_MARK,
            ReferenceItem.cod == cod,
            or_(ReferenceItem.tip2 == 0, ReferenceItem.tip2.is_(None)),
            ReferenceItem.flag_deleted.is_(False),
        )
        return await self.session.scalar(stmt)

    async def get_answer_options(self, questionnaire_cod: int) -> list[ReferenceItem]:
        stmt = (
            select(ReferenceItem)
            .where(
                ReferenceItem.ident == ANSWER_IDENT_SHIFT + questionnaire_cod,
                ReferenceItem.flag_deleted.is_(False),
            )
            .order_by(ReferenceItem.cod.asc().nulls_last(), ReferenceItem.name.asc().nulls_last())
        )
        return list((await self.session.scalars(stmt)).all())

    async def get_groups(self) -> list[ReferenceItem]:
        stmt = (
            select(ReferenceItem)
            .where(ReferenceItem.ident == QUESTION_GROUP_IDENT_MARK, ReferenceItem.flag_deleted.is_(False))
            .order_by(ReferenceItem.cod.asc().nulls_last())
        )
        return list((await self.session.scalars(stmt)).all())

    async def get_questions(self, questionnaire_cod: int) -> list[Question]:
        stmt = (
            select(Question)
            .where(
                Question.cod == QUESTION_CODE,
                Question.id_2 == questionnaire_cod,
                Question.count_4 == QUESTION_COUNT_4_MARK,
            )
            .order_by(Question.count_1.asc().nulls_last(), Question.id_1.asc().nulls_last())
        )
        return list((await self.session.scalars(stmt)).all())
