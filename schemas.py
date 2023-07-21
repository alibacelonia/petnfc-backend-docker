from pydantic import BaseModel, validator
from typing import List, Optional
from fastapi import HTTPException, status

from core.constants.role import Role
from core.constants.sex import Sex

        
class Pet(BaseModel):
    id: int
    name: str
    gender: str
    breed: str
    class Config():
        orm_mode = True
        
class PetBase(BaseModel):
    name: str
    breed: str
    gender: Sex
    owner_id: int
    
    @validator('gender')
    def validate_role(cls, gender):
        if gender not in [Sex.MALE, Sex.FEMALE]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid gender")
        return gender

class User(BaseModel):
    id: int
    username: str
    class Config():
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: str
    password: str
    role: Optional[Role] = Role.USER
    is_active: Optional[bool] = True
    
    @validator('role')
    def validate_role(cls, role):
        if role not in [Role.ADMIN, Role.USER]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")
        return role
    
    class Config():
        orm_mode = True
    
class UserDisplay(BaseModel):
    username: str
    email: str
    password: str
    role: str
    is_active: bool
    pets: List[Pet] = []
    class Config():
        orm_mode = True
    
class PetDisplay(BaseModel):
    id: int
    name: str
    gender: str
    breed: str
    owner: User
    class Config():
        orm_mode = True