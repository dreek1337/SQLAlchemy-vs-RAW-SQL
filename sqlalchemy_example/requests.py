from sqlalchemy import (
    func,
    select,
    delete
)
from sqlalchemy.orm import Session

from sqlalchemy_example.db_settings import engine
from sqlalchemy_example.models import (
    Questions,
    Choices
)

with Session(engine) as conn:
    """
    Создание вопросов и очистка бд перед созданием
    """
    delete_questions = conn.execute(delete(Questions))

    questions_text = [
        'Сколько стоит руль?',
        'Сколько стоит колесо?',
        'Сколько стоит рама?'
    ]

    new_questions = [
        Questions(question_text=text) for text in questions_text
    ]

    conn.add_all(new_questions)

    conn.commit()

with Session(engine) as conn:
    """
    Создание вопросов
    """
    all_questions = conn.scalars(select(Questions.question_id)).all()
    choices_of_question = (
        Choices(
            choice_text='Руль стоит 250р',
            votes=256,
            question_id=all_questions[0]
        ),
        Choices(
            choice_text='Руль стоит 270р',
            votes=456,
            question_id=all_questions[0]
        ),
        Choices(
            choice_text='Колесо стоит 280р',
            votes=13,
            question_id=all_questions[1]
        ),
        Choices(
            choice_text='Колесо стоит 290р',
            votes=165,
            question_id=all_questions[1]
        ),
        Choices(
            choice_text='Колесо стоит 285р',
            votes=1432,
            question_id=all_questions[1]
        ),
        Choices(
            choice_text='Рама стоит 289р',
            votes=1,
            question_id=all_questions[2]
        ),
        Choices(
            choice_text='Рама стоит 291р',
            votes=15,
            question_id=all_questions[2]
        ),
        Choices(
            choice_text='Рама стоит 2889р',
            votes=14329,
            question_id=all_questions[2]
        ),
        Choices(
            choice_text='Рама стоит 28р',
            votes=12,
            question_id=all_questions[2]
        )
    )

    conn.add_all(choices_of_question)

    conn.commit()

with Session(engine) as conn:
    """
    Кол-во вопросов/вариантов овтетов
    """
    query_questions = select(func.count(Questions.question_id))
    query_choices = select(func.count(Choices.choice_id))
    result_q = conn.scalar(query_questions)
    result_c = conn.scalar(query_choices)
    print('Кол-во вопросов составлет:', result_q)
    print('Кол-во варинтов ответа составлет:', result_c)

with Session(engine) as conn:
    """
    Кол-во ответов на каждый вопрос
    """
    query = (
        select(Questions.question_text, func.count(Choices.choice_id))
        .join(Choices.question)
        .group_by(Questions.question_id)
    )

    result = conn.execute(query).fetchall()

    print('Кол-во вариантов ответов на каждый вопрос:', result)

with Session(engine) as conn:
    """
    Сумма ответов на каждый вопрос
    """
    query = (
        select(Questions.question_text, func.sum(Choices.votes))
        .join(Choices.question)
        .group_by(Questions.question_text)
    )

    result = conn.execute(query).fetchall()

    print("Кол-во голосов на каждый вопрос составляет:", result)
