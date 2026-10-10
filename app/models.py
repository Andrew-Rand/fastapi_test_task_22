import uuid

from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ReferenceItem(Base):
    __tablename__ = "reference_items"

    uid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    ident: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    cod: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    tip2: Mapped[int | None] = mapped_column(Integer, nullable=True)
    flag_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class Question(Base):
    __tablename__ = "questions"

    uid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    cod: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    id_1: Mapped[int | None] = mapped_column(Integer, nullable=True)
    id_2: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    count_1: Mapped[int | None] = mapped_column(Integer, nullable=True)
    count_5: Mapped[int | None] = mapped_column(Integer, nullable=True)
    str_1: Mapped[str | None] = mapped_column(String(60), nullable=True)
    text_1: Mapped[str | None] = mapped_column(Text, nullable=True)
    boolean_1: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    count_4: Mapped[int | None] = mapped_column(Integer, nullable=True)
