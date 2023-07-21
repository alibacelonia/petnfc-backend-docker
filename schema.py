from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class RoleBase(BaseModel):
    role_name: str

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    pass

class Role(RoleBase):
    role_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    password: str
    first_name: str
    last_name: str
    birth_date: datetime
    address: str
    phone_number: str
    is_verified: Optional[bool]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserDisplayPublic(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: str = None
    address: Optional[str] = None
    
    class Config:
        orm_mode = True

class UserCreate(UserBase):
    roles: List[RoleCreate]

class UserUpdateDetails(UserBase):
    pass

class UserUpdatePassword(BaseModel):
    password: str

class User(UserBase):
    user_id: int
    roles: List[Role]

    class Config:
        orm_mode = True
        
class PetTypeBase(BaseModel):
    type: str
        
    class Config:
        orm_mode = True
        
class PetTypeDetails(PetTypeBase):
    type_id: int
    type: str
    # created_at: datetime
    # updated_at: datetime
        
    class Config:
        orm_mode = True
        
class PetBase(BaseModel):
    name: str = None
    gender: str = None
    pet_type_id: int = None
    breed: str = None
    color: str = None
    date_of_birth_month: int = None
    date_of_birth_year: int = None
    owner_id: int = None
    
    class Config:
        orm_mode = True
        
class PetCreate(PetBase):
    created_at: Optional[datetime]

class PetUpdate(PetBase):
    updated_at: Optional[datetime]

class Pet(PetBase):
    pet_id: int

    class Config:
        orm_mode = True

class PetUnique(BaseModel):
    unique_id: UUID = None
    
    class Config:
        orm_mode = True

class PetPublicDisplay(BaseModel):
    pet: PetBase = None
    owner: UserDisplayPublic = None
    
    class Config:
        orm_mode = True

class PetDetails(PetBase):
    pet_id: int= None
    unique_id: UUID = None

    class Config:
        orm_mode = True

class PaymentDetailsBase(BaseModel):
    payment_method: str
    card_number: str
    card_expiry: str
    card_cvv: str
    billing_address: str
    amount: int
    currency: str
    

    class Config:
        orm_mode = True

class PaymentDetailsCreate(PaymentDetailsBase):
    pass

class PaymentDetailsUpdate(PaymentDetailsBase):
    pass

class PaymentDetails(PaymentDetailsBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class SubscriptionPlanBase(BaseModel):
    name: str
    description: str
    price: int
    duration: str
    features: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    trial_period: Optional[int]
    max_users: Optional[int]
    limits: Optional[str]
    

    class Config:
        orm_mode = True

class SubscriptionPlanCreate(SubscriptionPlanBase):
    pass

class SubscriptionPlanUpdate(SubscriptionPlanBase):
    pass

class SubscriptionPlan(SubscriptionPlanBase):
    id: int

    class Config:
        orm_mode = True

class SubscriptionBase(BaseModel):
    user_id: int
    plan_id: int
    start_date: datetime
    end_date: datetime
    

    class Config:
        orm_mode = True

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(SubscriptionBase):
    pass

class Subscription(SubscriptionBase):
    id: int

    class Config:
        orm_mode = True

class ReviewBase(BaseModel):
    rating: int
    comment: str
    

    class Config:
        orm_mode = True

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    reviewer_id: int
    reviewee_id: int

    class Config:
        orm_mode = True
