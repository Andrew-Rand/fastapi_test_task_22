import json
from pathlib import Path
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.quests.models import Question, ReferenceItem


def _uuid(value: str) -> UUID:
    # For correct integrity checking
    return UUID(value)


async def seed_data(session: AsyncSession, data_dir: str) -> None:
    directory = Path(data_dir)
    reference_path = directory / "reference_items_.json"
    questions_path = directory / "questions.json"

    with reference_path.open(encoding="utf-8") as file:
        reference_data = json.load(file)["reference_items"]
    with questions_path.open(encoding="utf-8") as file:
        question_data = json.load(file)["questions"]

    existing_refs = set((await session.scalars(select(ReferenceItem.uid))).all())
    existing_questions = set((await session.scalars(select(Question.uid))).all())

    for row in reference_data:
        uid = _uuid(row["UID"])
        if uid in existing_refs:
            continue
        session.add(
            ReferenceItem(
                uid=uid,
                ident=row["Ident"],
                cod=row.get("Cod"),
                name=row.get("Name"),
                tip2=row.get("Tip2"),
                flag_deleted=row.get("FlagDeleted", False),
            )
        )

    for row in question_data:
        uid = _uuid(row["UID"])
        if uid in existing_questions:
            continue
        session.add(
            Question(
                uid=uid,
                cod=row.get("Cod"),
                id_1=row.get("ID_1"),
                id_2=row.get("ID_2"),
                count_1=row.get("Count_1"),
                count_5=row.get("Count_5"),
                str_1=row.get("STR_1"),
                text_1=row.get("Text_1"),
                boolean_1=row.get("Boolean_1"),
                count_4=row.get("Count_4"),
            )
        )

    await session.commit()
