from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer, Boolean
from core.db.database import Base
from sqlalchemy import Column, DateTime
from core.constants.sex import Sex

class DBDocuments(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, unique=True, nullable=False)
    file_type = Column(String)
    file_url = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("DBUsers", back_populates="documents")
    
    created_date = Column(DateTime, default=datetime.now())
    modified_date = Column(DateTime)
    