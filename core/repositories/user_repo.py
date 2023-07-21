from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
from core.db.hash import Hash
from core.model.models import User

from schema import UserBase, UserUpdateDetails, UserUpdatePassword, UserCreate

from sqlalchemy.exc import IntegrityError

def create_user(db: Session, request: UserBase):
    new_user = User(
        username=request.username,
        password=Hash.bcrypt(request.password),
        email=request.email,
        first_name=request.first_name,
        last_name=request.last_name,
        birth_date=request.birth_date,
        address=request.address,
        phone_number=request.phone_number,
        is_verified=request.is_verified,
        created_at=request.created_at,
        updated_at=request.updated_at
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": "Duplicate user"})
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.WS_1011_INTERNAL_ERROR, detail=str(e))
    
def get_all_users(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, id: int):
    user = db.query(User).filter(User.user_id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

def get_user_by_username(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

def update_user_details(db: Session, id: int, request: UserUpdateDetails):
    user = db.query(User).filter(User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user.update({
        User.password: Hash.bcrypt(request.password),
        User.first_name: request.first_name,
        User.last_name: request.last_name,
        User.birth_date: request.birth_date,
        User.address: request.address,
        User.phone_number: request.phone_number,
        User.is_verified: request.is_verified
    })
    
    try:
        db.commit()
        return "OK"
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message": "Something went wrong"})

def update_user_password(db: Session, id: int, request: UserUpdatePassword):
    user = db.query(User).filter(User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user.update({
        User.password: Hash.bcrypt(request.password)
    })
    
    try:
        db.commit()
        return "OK"
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message": "Something went wrong"})