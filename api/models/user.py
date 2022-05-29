from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from api.database import Base


class UserModel(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable =False, server_default = text('now()'))
