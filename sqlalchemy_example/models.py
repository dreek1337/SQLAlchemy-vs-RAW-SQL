from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)
from sqlalchemy import (
    String,
    Integer,
    BigInteger,
    ForeignKey
)


class Base(DeclarativeBase):
    pass


class Questions(Base):
    __tablename__ = "questions"

    question_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )
    question_text: Mapped[str] = mapped_column(String(150))

    choices: Mapped[list["Choices"]] = relationship(
        back_populates="question",
        cascade="all, delete-orphan"
    )


class Choices(Base):
    __tablename__ = "choices"

    choice_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )
    choice_text: Mapped[str] = mapped_column(String(50))
    votes: Mapped[int] = mapped_column(Integer)
    question_id: Mapped[int] = mapped_column(
        ForeignKey(
            "questions.question_id",
            ondelete="CASCADE"
        )
    )

    question: Mapped["Questions"] = relationship(back_populates="choices")
