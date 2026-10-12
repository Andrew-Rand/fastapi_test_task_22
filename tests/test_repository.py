from typing import Any

import pytest
from sqlalchemy.dialects import postgresql

from app.quests.repository import QuestionnaireRepository


class ScalarRows:
    def __init__(self, rows: list[Any]) -> None:
        self.rows = rows

    def all(self) -> list[Any]:
        return self.rows


class FakeAsyncSession:
    def __init__(
        self,
        *,
        rows: list[Any] | None = None,
        scalar_result: Any = None,
    ) -> None:
        self.rows = rows or []
        self.scalar_result = scalar_result
        self.statement = None

    async def scalars(self, statement: Any) -> ScalarRows:
        self.statement = statement
        return ScalarRows(self.rows)

    async def scalar(self, statement: Any) -> Any:
        self.statement = statement
        return self.scalar_result


def get_sql(statement: Any) -> str:
    return str(
        statement.compile(
            dialect=postgresql.dialect(),
            compile_kwargs={"literal_binds": True},
        )
    )


class TestListAvailable:
    @pytest.mark.asyncio
    async def test_list_available_if_ok(self) -> None:
        session = FakeAsyncSession(rows=["row"])

        result = await QuestionnaireRepository(session).list_available()
        sql = get_sql(session.statement)

        assert result == ["row"]
        assert "43005" in sql
        assert "IS NULL" in sql
        assert "= 0" in sql
        assert "IS false" in sql
        assert "ORDER BY" in sql
        assert "NULLS LAST" in sql


class TestGetQuestionnaire:
    @pytest.mark.asyncio
    async def test_get_questionnaire_if_ok(self) -> None:
        session = FakeAsyncSession(scalar_result="questionnaire")

        result = await QuestionnaireRepository(session).get_questionnaire(12)
        sql = get_sql(session.statement)

        assert result == "questionnaire"
        assert "43005" in sql
        assert "= 12" in sql
        assert "IS false" in sql
        assert "IS NULL" in sql


class TestGetAnswerOptions:
    @pytest.mark.asyncio
    async def test_get_answer_options_if_ok(self) -> None:
        session = FakeAsyncSession(rows=["option"])

        result = await QuestionnaireRepository(session).get_answer_options(3)
        sql = get_sql(session.statement)

        assert result == ["option"]
        assert "79003" in sql
        assert "IS false" in sql
        assert "ORDER BY" in sql


class TestGetGroups:
    @pytest.mark.asyncio
    async def test_get_groups_if_ok(self) -> None:
        session = FakeAsyncSession(rows=["group"])

        result = await QuestionnaireRepository(session).get_groups()
        sql = get_sql(session.statement)

        assert result == ["group"]
        assert "43010" in sql
        assert "IS false" in sql
        assert "ORDER BY" in sql


class TestGetQuestions:
    @pytest.mark.asyncio
    async def test_get_questions_if_ok(self) -> None:
        session = FakeAsyncSession(rows=["question"])

        result = await QuestionnaireRepository(session).get_questions(3)
        sql = get_sql(session.statement)

        assert result == ["question"]
        assert "= 41" in sql
        assert "= 3" in sql
        assert "= 0" in sql
        assert "ORDER BY" in sql
