from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base


class Todo(Base):
    __tablename__ = "todos"

    id        = Column(Integer, primary_key=True, index=True)
    title     = Column(String(200), nullable=False)
    desc      = Column(String(500), default="")
    priority  = Column(String(10), default="medium")   # low / medium / high
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
