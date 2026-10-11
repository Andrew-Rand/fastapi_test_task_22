from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest

from app.service import QuestionnaireNotFound, QuestionnaireUseCase


def reference_item(
    *,
    cod: int | None = None,
    name: str | None = None,
    ident: int = 43005,
    uid: UUID | None = None,
    tip2: int | None = 0,
    flag_deleted: bool = False,
) -> SimpleNamespace:
    return SimpleNamespace(
        uid=uid or uuid4(),
        ident=ident,
        cod=cod,
        name=name,
        tip2=tip2,
        flag_deleted=flag_deleted,
    )


def question(
    *,
    group_cod: int | None = 0,
    question_id: int = 1,
    order: int = 1,
    required: bool | None = None,
    short_text: str = "Short question",
    text: str = "Full question text",
    uid: UUID | None = None,
) -> SimpleNamespace:
    return SimpleNamespace(
        uid=uid or uuid4(),
        id_1=question_id,
        count_1=order,
        count_5=group_cod,
        str_1=short_text,
        text_1=text,
        boolean_1=required,
    )


class TestListQuestionnaires:
    @pytest.mark.asyncio
    async def test_list_questionnaires_if_ok(self) -> None:
        first = reference_item(cod=2, name=None)
        second = reference_item(cod=1, name="First")
        missing_cod = reference_item(cod=None, name="Invalid")
        repository = AsyncMock()
        repository.list_available.return_value = [first, second, missing_cod]

        result = await QuestionnaireUseCase(repository).get_list()

        assert [(item.cod, item.name) for item in result] == [(2, ""), (1, "First")]
        repository.list_available.assert_awaited_once_with()


class TestGetQuestionnaire:
    @pytest.mark.asyncio
    async def test_get_questionnaire_if_ok(self) -> None:
        questionnaire_record = reference_item(cod=7, name="Questionnaire")
        options = [
            reference_item(cod=1, name="Yes", ident=79007),
            reference_item(cod=0, name="No", ident=79007),
        ]
        group_records = [
            reference_item(cod=20, name="Second group", ident=43010),
            reference_item(cod=10, name="First group", ident=43010),
            reference_item(cod=None, name="Ignored", ident=43010),
        ]
        ungrouped_zero = question(group_cod=0, question_id=101, order=1, required=True)
        grouped_later = question(group_cod=20, question_id=202, order=4)
        grouped_first = question(group_cod=10, question_id=303, order=2, required=False)
        ungrouped_null = question(group_cod=None, question_id=404, order=3, required=True)
        missing_group = question(group_cod=999, question_id=505, order=5, required=True)

        repository = AsyncMock()
        repository.get_questionnaire.return_value = questionnaire_record
        repository.get_answer_options.return_value = options
        repository.get_groups.return_value = group_records
        repository.get_questions.return_value = [
            ungrouped_zero,
            grouped_later,
            grouped_first,
            ungrouped_null,
            missing_group,
        ]

        result = await QuestionnaireUseCase(repository).get_item(7)

        assert result.cod == 7
        assert result.name == "Questionnaire"
        assert [(item.cod, item.value) for item in result.answer_options] == [
            (1, "Yes"),
            (0, "No"),
        ]
        assert [group.cod for group in result.groups] == [None, 10, 20]
        assert result.groups[0].name is None
        assert [item.id for item in result.groups[0].questions] == [101, 404]
        assert [item.id for item in result.groups[1].questions] == [303]
        assert [item.id for item in result.groups[2].questions] == [202]
        assert result.groups[0].questions[0].required is True
        assert result.groups[0].questions[1].required is True
        assert result.groups[1].questions[0].required is False
        assert all(
            item.id != 505
            for group in result.groups
            for item in group.questions
        )
        repository.get_questionnaire.assert_awaited_once_with(7)
        repository.get_answer_options.assert_awaited_once_with(7)
        repository.get_groups.assert_awaited_once_with()
        repository.get_questions.assert_awaited_once_with(7)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "questionnaire_record",
        [None, reference_item(cod=None, name="No code")],
    )
    async def test_get_questionnaire_if_not_found(
        self,
        questionnaire_record: SimpleNamespace | None,
    ) -> None:
        repository = AsyncMock()
        repository.get_questionnaire.return_value = questionnaire_record

        with pytest.raises(QuestionnaireNotFound):
            await QuestionnaireUseCase(repository).get_item(123)

        repository.get_answer_options.assert_not_awaited()
        repository.get_groups.assert_not_awaited()
        repository.get_questions.assert_not_awaited()
