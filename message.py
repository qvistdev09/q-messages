from datetime import datetime
from db import Base
from sqlalchemy import Column, ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property


class Message(Base):
    __tablename__ = "messages"
    id = Column("id", Integer, primary_key=True)
    body = Column("body", String(5000), nullable=False)
    nickname = Column("nickname", String(255), nullable=False)
    author_sub = Column("author_sub", String(255), nullable=False)
    created_at = Column("created_at", DateTime(timezone=True), nullable=False)
    parent_message = Column("parent_message", Integer,
                            ForeignKey("messages.id"))
    children = relationship("Message")

    @hybrid_property
    def readable_date(self):
        return self.created_at.strftime("%H:%M %B %d, %Y")

    def __init__(self, body: str, nickname: str, author_sub: str, created_at: datetime):
        self.body = body
        self.nickname = nickname
        self.author_sub = author_sub
        self.created_at = created_at
