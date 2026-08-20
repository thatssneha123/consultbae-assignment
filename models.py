from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Boolean
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True)

    name = Column(String)
    email = Column(String)
    phone = Column(String)
    city = Column(String)

    experience = Column(Float)
    current_ctc = Column(Float)
    applied_date = Column(String)

    skills = Column(String)

    hourly_rate = Column(String)
    worker_status = Column(String)

    verified = Column(Boolean)
    projects_completed = Column(Integer)

    source = Column(String)


engine = create_engine("sqlite:///database/consultbae.db")

Base.metadata.create_all(engine)