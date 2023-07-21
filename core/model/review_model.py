from datetime import datetime
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer
from core.db.database import Base
from sqlalchemy import ARRAY, Column, DateTime
from sqlalchemy.orm import relationship

class PetWalkerReview(Base):
    __tablename__ = 'pet_walker_reviews'

    review_id = Column(Integer, primary_key=True)
    pet_walker_id = Column(Integer, ForeignKey('pet_walkers.pet_walker_id'))
    pet_owner_id = Column(Integer, ForeignKey('pet_owners.pet_owner_id'))
    rating = Column(Integer)
    review_text = Column(String(500))
    review_date = Column(DateTime, default=datetime.now())

    images = relationship('ReviewImage')
    
class ReviewImage(Base):
    __tablename__ = 'review_images'

    image_id = Column(Integer, primary_key=True)
    review_id = Column(Integer, ForeignKey('pet_walker_reviews.review_id'))
    image_url = Column(String(255))