from collections import defaultdict

from app.quests.repository import QuestionnaireRepository
from app.quests.schemas import (
    AnswerOption,
    QuestionGroup,
    QuestionOut,
    QuestionnaireDetail,
    QuestionnaireShort,
)


class QuestionnaireNotFound(Exception):
    pass


class QuestionnaireUseCase:
    # TODO: maybe add base class with get_list and get_item
    def __init__(self, repository: QuestionnaireRepository):
        self.repository = repository

    async def get_list(self) -> list[QuestionnaireShort]:
        records = await self.repository.list_available()
        return [
            QuestionnaireShort(uid=item.uid, cod=item.cod, name=item.name or "")
            for item in records
            if item.cod is not None
        ]

    async def get_item(self, cod: int) -> QuestionnaireDetail:
        questionnaire = await self.repository.get_questionnaire(cod)
        if not questionnaire or questionnaire.cod is None:
            raise QuestionnaireNotFound

        options = await self.repository.get_answer_options(cod)
        group_records = await self.repository.get_groups()
        questions = await self.repository.get_questions(cod)

        # collect questions with group name
        group_names = {
            item.cod: item.name
            for item in group_records
            if item.cod is not None
        }

        questions_by_group: dict[int | None, list[QuestionOut]] = defaultdict(list)

        for question in questions:
            group_cod = question.count_5 or None

            if group_cod is not None and group_cod not in group_names:
                continue

            questions_by_group[group_cod].append(
                QuestionOut(
                    uid=question.uid,
                    id=question.id_1,
                    order=question.count_1,
                    short_text=question.str_1,
                    text=question.text_1,
                    required=question.boolean_1 is True,
                )
            )

        groups = []

        for group_cod, group_questions in sorted(
                questions_by_group.items(),
                key=lambda item: (item[0] is not None, item[0] or 0),
        ):
            groups.append(
                QuestionGroup(
                    cod=group_cod,
                    name=group_names.get(group_cod) if group_cod is not None else None,
                    questions=group_questions,
                )
            )

        return QuestionnaireDetail(
            uid=questionnaire.uid,
            cod=cod,
            name=questionnaire.name or "",
            answer_options=[
                AnswerOption(uid=item.uid, cod=item.cod, value=item.name)
                for item in options
            ],
            groups=groups,
        )
