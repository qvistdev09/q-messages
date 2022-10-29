from datetime import datetime
from db import Base
from sqlalchemy import Column, String, Integer, DateTime


class Message(Base):
    __tablename__ = "messages"
    id = Column("id", Integer, primary_key=True)
    body = Column("body", String(255), nullable=False)
    nickname = Column("nickname", String(255), nullable=False)
    author_sub = Column("author_sub", String(255), nullable=False)
    created_at = Column("created_at", DateTime(timezone=True), nullable=False)

    def __init__(self, body: str, nickname: str, author_sub: str, created_at: datetime):
        self.body = body
        self.nickname = nickname
        self.author_sub = author_sub
        self.created_at = created_at
