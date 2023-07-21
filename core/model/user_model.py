from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer, Boolean
from core.db.database import Base
from sqlalchemy import Column
from core.constants.role import Role

class DBUsers(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email =  Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    
    firstname = Column(String)
    lastname = Column(String)
    address = Column(String)
    birthday = Column(String)
    gender = Column(String)
    phone_number = Column(String)
    
    documents = relationship("DBDocuments", back_populates="owner")
    
    role = Column(String, default=Role.USER)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    pets = relationship("DBPets", back_populates="owner")
    
    