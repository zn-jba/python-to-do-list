from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self) -> str:
        return self.task

    @staticmethod
    def add_task(task: str, date: str = "") -> None:
        if not date:
            date = datetime.today().strftime("%m-%d-%Y")
        new_row = Task(task=task,
                       deadline=datetime.strptime(date, "%Y-%m-%d").date())
        session.add(new_row)
        session.commit()

    @staticmethod
    def delete_task(row: int) -> None:
        if rows := Task.find_all(sort_by_date=True):
            session.delete(rows[row])
            session.commit()

    @staticmethod
    def missed_tasks() -> list["Task"]:
        return session.query(Task).filter(
            Task.deadline < datetime.today().date()).order_by(Task.deadline).all()

    @staticmethod
    def find_all(sort_by_date: bool = False) -> list["Task"]:
        if sort_by_date:
            return session.query(Task).order_by(Task.deadline).all()
        return session.query(Task).all()

    @staticmethod
    def find_tasks_by_date(date_obj: datetime) -> list["Task"]:
        return session.query(Task).filter(Task.deadline == date_obj.date()).all()

    @staticmethod
    def find_tasks_by_range(start: datetime, end: datetime) -> list["Task"]:
        return session.query(Task).filter(
            start.date() <= Task.deadline <= end.date()).all()


FILE_NAME = "todo.db"

engine = create_engine(f"sqlite:///{FILE_NAME}?check_same_thread=False")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
