from sqlalchemy import String, Column, Date, BigInteger

from db import base


class Task(base):
    __tablename__ = 'task'

    task_id = Column(BigInteger, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    date = Column(Date, nullable=False)

    def __str__(self):
        return 'Task(taskId={},title={},description={},date={})' \
            .format(self.taskId, self.title, self.description, self.date)

    def __eq__(self, other):
        if isinstance(other, Task):
            return self.task_id == other.task_id \
                   and self.title == other.title \
                   and self.description == other.description \
                   and self.date == other.date

        return False
