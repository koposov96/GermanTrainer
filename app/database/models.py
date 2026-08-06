from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Word(Base):

    __tablename__ = "words"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    telegram_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )


    german: Mapped[str] = mapped_column(
        String,
        nullable=False
    )


    russian: Mapped[str] = mapped_column(
        String,
        nullable=False
    )


    category: Mapped[str] = mapped_column(
        String,
        default="Общие слова"
    )


    lesson: Mapped[str] = mapped_column(
        String,
        default="Без категории"
    )