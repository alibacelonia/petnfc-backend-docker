from uuid import uuid4
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer, Boolean, DateTime, JSON, Text, Numeric
from core.db.database import Base
from sqlalchemy import Column, Table
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
# user_subscription_association = Table(
#     'user_subscription_association',
#     Base.metadata,
#     Column('user_id', Integer, ForeignKey('users.user_id')),
#     Column('subscription_plan_id', Integer, ForeignKey('subscription_plans.id'))
# )

# user_pet_association = Table(
#     'user_pet_association',
#     Base.metadata,
#     Column('user_id', Integer, ForeignKey('users.user_id')),
#     Column('pet_id', Integer, ForeignKey('pets.pet_id'))
# )

class Roles(Base):
    __tablename__ = 'roles'
    role_id = Column(Integer, primary_key=True)
    role_name = Column(String(50), nullable=False)
    
    users = relationship('UserRoles', back_populates='role')

class UserRoles(Base):
    __tablename__ = 'user_roles'
    user_id = Column(Integer, ForeignKey('users.user_id'), default=None, primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.role_id'), default=None, primary_key=True)
 
    user = relationship('User', back_populates='roles')
    role = relationship('Roles', back_populates='users')
    
class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    address = Column(String(255))
    post_code = Column(String(10))
    phone_number = Column(String(20))
    secondary_contact = Column(String(255))
    secondary_contact_number = Column(String(255))
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())

    payment_details = relationship('PaymentDetails', back_populates='user')
    subscriptions = relationship('Subscription', back_populates='user')
    reviews_given = relationship('Review', back_populates='reviewer', foreign_keys='Review.reviewer_id')
    reviews_received = relationship('Review', back_populates='reviewee', foreign_keys='Review.reviewee_id')
    pets = relationship('Pet', back_populates='owners')
    roles = relationship('UserRoles', back_populates='user')

class PetType(Base):
    __tablename__ = 'pet_types'

    type_id = Column(Integer, primary_key=True)
    type = Column(String(255), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())

    pets = relationship('Pet', back_populates='pet_type')

class Pet(Base):
    __tablename__ = 'pets'

    pet_id = Column(Integer, primary_key=True)
    unique_id = Column(UUID(as_uuid=True), default=uuid.uuid4, server_default='gen_random_uuid()')
    microchip_id = Column(String(50), unique=True, nullable=True)
    name = Column(String(255))
    gender = Column(String(20))
    color = Column(String(255))
    pet_type_id = Column(Integer, ForeignKey('pet_types.type_id'))
    pet_type = relationship('PetType', back_populates='pets')
    breed = Column(String(255))
    date_of_birth_month = Column(Integer)
    date_of_birth_year = Column(Integer)
    owner_id = Column(Integer, ForeignKey('users.user_id'))
    owners = relationship('User', back_populates='pets')
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())
    
    @property
    def date_of_birth(self):
        if self.date_of_birth_month and self.date_of_birth_year:
            return datetime(self.date_of_birth_year, self.date_of_birth_month, 1).date()
        return None

    @date_of_birth.setter
    def date_of_birth(self, value):
        if value:
            self.date_of_birth_month = value.month
            self.date_of_birth_year = value.year
        else:
            self.date_of_birth_month = None
            self.date_of_birth_year = None
   
class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    reviewer_id = Column(Integer, ForeignKey('users.user_id'))
    reviewee_id = Column(Integer, ForeignKey('users.user_id'))
    rating = Column(Integer)
    comment = Column(String(255))
    created_at = Column(DateTime, default=datetime.now())

    reviewer = relationship('User', foreign_keys=[reviewer_id], back_populates='reviews_given')
    reviewee = relationship('User', foreign_keys=[reviewee_id], back_populates='reviews_received')
    
    
class PaymentDetails(Base):
    __tablename__ = 'payment_details'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    payment_method = Column(String(255))
    card_number = Column(String(255))
    card_expiry = Column(String(255))
    card_cvv = Column(String(255))
    billing_address = Column(String(255))
    amount = Column(Integer)
    currency = Column(String(255))

    user = relationship('User', back_populates='payment_details')
    
class SubscriptionPlan(Base):
    __tablename__ = 'subscription_plans'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    price = Column(Integer, nullable=False)
    duration = Column(String(255))
    features = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime, onupdate=datetime.utcnow())
    trial_period = Column(Integer)
    max_users = Column(Integer)
    limits = Column(Text)

    subscriptions = relationship('Subscription', back_populates='plan')
    
class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    plan_id = Column(Integer, ForeignKey('subscription_plans.id'))
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    user = relationship('User', back_populates='subscriptions')
    plan = relationship('SubscriptionPlan', back_populates='subscriptions')

    
class AuditTrail(Base):
    __tablename__ = 'audit_trail'

    id = Column(Integer, primary_key=True)
    event_timestamp = Column(DateTime, nullable=False)
    user_id = Column(Integer)
    event_description = Column(String)
    ip_address = Column(String)
    additional_data = Column(Text)
    
class LogEntry(Base):
    __tablename__ = 'log_entries'

    id = Column(Integer, primary_key=True)
    log_timestamp = Column(DateTime, nullable=False)
    log_level = Column(String, nullable=False)
    log_message = Column(Text)