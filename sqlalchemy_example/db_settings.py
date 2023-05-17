from sqlalchemy import create_engine

from sqlalchemy_example.models import Base

engine = create_engine('postgresql+psycopg2://postgresql:danil1337danil@localhost:5432/mydb', echo=True)

Base.metadata.create_all(engine)
