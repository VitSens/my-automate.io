from sqlalchemy import Column, JSON, String

from db.db import base


class Token(base):
    __tablename__ = 'token'

    id = Column(String, primary_key=True)
    token = Column(JSON)

    def __str__(self):
        return 'Token(id={},token={})'.format(self.id, self.token)
