import sys
from types import ModuleType, SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.quests.schemas import QuestionnaireShort, QuestionnaireDetail, AnswerOption, QuestionGroup

# API unit tests don't require a database driver or a running PostgreSQL instance.
_fake_db = ModuleType("app.db")
_fake_db.SessionFactory = MagicMock(name="SessionFactory")
_fake_db.engine = SimpleNamespace(dispose=AsyncMock())


async def unused_get_session():
    yield None


_fake_db.get_session = unused_get_session
sys.modules["app.core.db"] = _fake_db

from app.main import app
from app.core.dependencies import get_use_case


class FakeService:
    async def get_list(self) -> list[QuestionnaireShort]:
        return [
            QuestionnaireShort(
                uid=uuid4(),
                cod=3,
                name="Questionnaire 3",
            )
        ]

    async def get_item(self, cod: int) -> QuestionnaireDetail:
        assert cod == 3
        return QuestionnaireDetail(
            uid=uuid4(),
            cod=3,
            name="Questionnaire 3",
            answer_options=[
                AnswerOption(uid=uuid4(), cod=1, value="Yes")
            ],
            groups=[QuestionGroup(cod=None, name=None, questions=[])],
        )


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    app.dependency_overrides.clear()
    app.dependency_overrides[get_use_case] = lambda: FakeService()
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client
    app.dependency_overrides.clear()
