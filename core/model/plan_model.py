from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer, Boolean, Double, JSON, DateTime
from core.db.database import Base
from sqlalchemy import Column
from core.constants.sex import Sex

class DBPlans(Base):
    __tablename__ = 'subscription_plans'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Double, nullable=False)
    duration = Column(String)
    features = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    trial_period = Column(Integer)
    max_users = Column(Integer)
    limits = Column(JSON)
    
    """
        id: A unique identifier for each plan or subscription.
        name: The name or title of the plan.
        description: A description or summary of the plan.
        price: The cost of the plan.
        duration: The duration of the subscription (e.g., monthly, yearly).
        features: A column to store the features or benefits associated with the plan. This could be an array, a JSON object, or a separate table to represent a many-to-many relationship with features.
        is_active: A flag indicating whether the plan is currently active or available for purchase.
        created_at and updated_at: Timestamps to track when the plan was created and last updated.
        trial_period: The length of the trial period for the plan, if applicable.
        max_users: The maximum number of users allowed for the plan.
        limits: Any specific usage limits or quotas associated with the plan (e.g., maximum storage, API calls).
    """