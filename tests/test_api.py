import pytest
from httpx import AsyncClient


class TestHealth:
    @pytest.mark.asyncio
    async def test_health_if_ok(self, async_client: AsyncClient) -> None:
        resp = await async_client.get("/health")

        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}


class TestQuestionnaireList:
    @pytest.mark.asyncio
    async def test_list_questionnaires_if_ok(self, async_client: AsyncClient) -> None:

        resp = await async_client.get("/api/v1/questionnaires")
        assert resp.status_code == 200

        data = resp.json()

        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["cod"] == 3
        assert data[0]["name"] == "Questionnaire 3"
        assert "uid" in data[0]


class TestGetQuestionnaire:
    @pytest.mark.asyncio
    async def test_get_questionnaire_if_ok(self, async_client: AsyncClient) -> None:

        resp = await async_client.get("/api/v1/questionnaires/3")
        assert resp.status_code == 200

        data = resp.json()

        assert data["cod"] == 3
        assert data["name"] == "Questionnaire 3"
        assert data["answer_options"][0]["value"] == "Yes"
        assert data["groups"][0]["cod"] is None
        assert data["groups"][0]["name"] is None

    class TestGetQuestionnaire:
        @pytest.mark.asyncio
        @pytest.mark.parametrize(
            "cod",
            [
                "not-an-integer",
                "abc",
                "1.5",
                " ",
                "null",
                "None",
                "true",
                None,
                1.2,
            ],
        )
        async def test_get_questionnaire_if_validation_error(
                self,
                async_client: AsyncClient,
                cod: str,
        ) -> None:
            resp = await async_client.get(f"/api/v1/questionnaires/{cod}")

            assert resp.status_code == 422
