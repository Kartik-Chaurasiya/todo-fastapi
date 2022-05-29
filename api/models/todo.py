from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP, Date
from sqlalchemy.sql.expression import text
from sqlalchemy.sql import func
from api.database import Base

class TodoModel(Base):
    __tablename__ = "todos"
    todo_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable =False)
    todo_text = Column(Text)
    todo_description = Column(Text, nullable=True)
    todo_complete_by = Column(Date, server_default=func.now())
    completed = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable =False, server_default = text('now()'))
    user = relationship("UserModel")
