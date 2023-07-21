from fastapi import HTTPException, status
from pydantic import ValidationError
from sqlalchemy import asc
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session
from core.db.hash import Hash
from core.model.models import Pet, User, PetType
from uuid import UUID

from schema import PetBase, PetPublicDisplay, PetTypeBase

from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse

# Get all pet types
def get_all_pet_types(db: Session):
    return db.query(PetType).order_by(asc(PetType.type_id)).all()

# Add pet type
def add_pet_type(db: Session, request: PetTypeBase):
    type = PetType(type=request.type)
    
    try:
        db.add(type, request)
        db.commit()
        db.refresh(type)
        return type
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message":"Duplicate Pet Type"})
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.WS_1011_INTERNAL_ERROR, detail=str(e))

# Update pet type
def update_pet_type(db: Session, id: int, request: PetTypeBase):
    pet_type = db.query(PetType).filter(PetType.type_id == id)
    if not pet_type.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet type not found")
    pet_type.update({
        PetType.type: request.type
    })
    db.commit()
    return ({"status_code": status.HTTP_200_OK, "detail": "Updated"}) 

# Get all pets
def get_all_pets(db: Session):
    return db.query(Pet).order_by(asc(Pet.pet_id)).all()

# Add new pet
def add_pet(db: Session, request: PetBase):
    new_pet = Pet(
        name=request.name,
        species=request.species,
        age=request.age,
        breed=request.breed,
        owner_id=request.owner_id
    )
    try:
        db.add(new_pet, request)
        db.commit()
        db.refresh(new_pet)
        return new_pet
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message":"Duplicate Pet"})
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.WS_1011_INTERNAL_ERROR, detail=str(e))

# Get pet by id
def get_pet_by_id(db: Session, pet_id: int):
    pet = db.query(Pet).filter(Pet.pet_id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
    return pet

# Get pet by unique id
def get_pet_by_unique_id(db: Session, unique_id: UUID):
    # pet = db.query(Pet).join(User).filter(Pet.unique_id == unique_id).first()
    pet = db.query(Pet).outerjoin(User).options(joinedload(Pet.owners)).filter(Pet.unique_id == unique_id).first()
    if not pet:
        return ({"status_code": status.HTTP_404_NOT_FOUND, "detail": "No record found"}) 
    # return pet
    return ({"status_code": status.HTTP_200_OK, "detail": "success", "data": PetPublicDisplay(pet=pet, owner=pet.owners)}) 


# Update pet
def update_pet(db: Session, id: UUID, request: PetBase):
    pet = db.query(Pet).filter(Pet.unique_id == id)
    if not pet.first():
        return ({"status_code": status.HTTP_404_NOT_FOUND, "detail": "No record found"}) 
    pet.update({
        Pet.name: request.name,
        Pet.gender: request.gender,
        Pet.pet_type_id: request.pet_type_id,
        Pet.breed: request.breed,
        Pet.date_of_birth_month: request.date_of_birth_month,
        Pet.date_of_birth_year: request.date_of_birth_year,
        Pet.owner_id: request.owner_id
    })
    db.commit()
    return ({"status_code": status.HTTP_200_OK, "detail": "success", "data": PetPublicDisplay(pet=pet, owner=pet.owners)}) 

def generate_qr(db: Session):
    return get_all_pets(db)