import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer, Boolean
from core.db.database import Base
from core.constants.sex import Sex

class DBPets(Base):
    __tablename__ = 'pets'
    id = Column(Integer, primary_key=True)
    uniqui_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default='gen_random_uuid()')
    name = Column(String, index=True, nullable=False)
    breed = Column(String, index=True, nullable=False)
    gender = Column(String, index=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("DBUsers", back_populates="pets")
    
    