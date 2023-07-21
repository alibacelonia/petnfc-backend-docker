from fastapi import APIRouter, Depends
from schema import UserCreate, UserBase, User
from sqlalchemy.orm import Session
from core.repositories import user_repo
from core.db.database import get_db
from typing import List

router = APIRouter(
    prefix='/user',
    tags=['user']
)

# Create a new user
@router.post('/', response_model=UserCreate)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return user_repo.create_user(db, request)

# Get users
@router.get('/', response_model=List[User])
def get_all_users(db: Session = Depends(get_db)):
    return user_repo.get_all_users(db)

# Get user by id
@router.get('/{id}', response_model=User)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    return user_repo.get_user_by_id(db, id)

# Get user by username
@router.get('/{username}', response_model=User)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    return user_repo.get_user_by_username(db, username)

# Update user
@router.post('/{id}/update')
def update_user_details(id: int, request: UserBase, db: Session = Depends(get_db)):
    return user_repo.update_user_details(db, id, request)