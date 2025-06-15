"""
Users are anyone who signs up. They can be members or not.
Users:
    - user_id int auto-increment primary key
    - email varchar(255) unique not null
    - password_hash varchar(255) not null
    - first_name varchar(50) not null
    - last_name varchar(50) not null
    - signup_date date not null
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date, datetime

from .. import schemas, models, crud
from ..deps import get_db

router = APIRouter()

@router.post("/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new user."""
    # Check for duplicate email
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user with signup date
    user_data = user.dict()
    user_data["signup_date"] = datetime.combine(date.today(), datetime.min.time())
    
    return crud.user.create(db, obj_in=schemas.UserCreate(**user_data))

@router.get("/{user_id}", response_model=schemas.UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user by ID."""
    user = crud.user.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.get("/", response_model=List[schemas.UserRead])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all users."""
    return crud.user.get_multi(db, skip=skip, limit=limit)

@router.get("/email/{email}", response_model=schemas.UserRead)
def read_user_by_email(email: str, db: Session = Depends(get_db)):
    """Get a specific user by email."""
    user = db.query(models.User).filter(
        models.User.email == email
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.put("/{user_id}", response_model=schemas.UserRead)
def update_user(
    user_id: int,
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """Update a user."""
    db_user = crud.user.get(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check for duplicate email
    existing_user = db.query(models.User).filter(
        models.User.user_id != user_id,
        models.User.email == user.email
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    return crud.user.update(db, db_obj=db_user, obj_in=user.dict())

@router.delete("/{user_id}", response_model=schemas.UserRead)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user."""
    user = crud.user.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if user has associated memberships or officer roles
    if user.memberships or user.officers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete user with associated memberships or officer roles"
        )
    
    return crud.user.remove(db, obj_id=user_id)
