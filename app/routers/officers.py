"""
Officers:
    - officer_id | int auto-increment primary key
    - user_id | int not null foreign key
    - role_id | int not null foreign key
    - start_date | datetime not null
    - end_date | datetime nullable
    - officer_image | mediumblob nullable
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models, crud
from ..deps import get_db

router = APIRouter()

@router.post("/", response_model=schemas.OfficerRead, status_code=status.HTTP_201_CREATED)
def create_officer(officer: schemas.OfficerCreate, db: Session = Depends(get_db)):
    """Create a new officer."""
    # Check if user exists
    user = crud.user.get(db, officer.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if role exists
    role = crud.role.get(db, officer.role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    
    # Check for overlapping officer periods
    overlapping_officer = db.query(models.Officer).filter(
        models.Officer.user_id == officer.user_id,
        ((models.Officer.start_date <= officer.start_date) & 
         (models.Officer.end_date >= officer.start_date)) |
        ((models.Officer.start_date <= officer.end_date) & 
         (models.Officer.end_date >= officer.end_date)) |
        ((models.Officer.start_date >= officer.start_date) & 
         (models.Officer.end_date <= officer.end_date))
    ).first()
    
    if overlapping_officer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already an officer during this period"
        )
    
    return crud.officer.create(db, obj_in=officer)

@router.get("/{officer_id}", response_model=schemas.OfficerRead)
def read_officer(officer_id: int, db: Session = Depends(get_db)):
    """Get a specific officer by ID."""
    officer = crud.officer.get(db, officer_id)
    if not officer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Officer not found"
        )
    return officer

@router.get("/", response_model=List[schemas.OfficerRead])
def list_officers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all officers."""
    return crud.officer.get_multi(db, skip=skip, limit=limit)

@router.get("/role/{role_id}", response_model=List[schemas.OfficerRead])
def list_role_officers(
    role_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all officers with a specific role."""
    # Check if role exists
    role = crud.role.get(db, role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    
    return db.query(models.Officer).filter(
        models.Officer.role_id == role_id
    ).offset(skip).limit(limit).all()

@router.put("/{officer_id}", response_model=schemas.OfficerRead)
def update_officer(
    officer_id: int,
    officer: schemas.OfficerCreate,
    db: Session = Depends(get_db)
):
    """Update an officer."""
    db_officer = crud.officer.get(db, officer_id)
    if not db_officer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Officer not found"
        )
    
    # Check for overlapping officer periods
    overlapping_officer = db.query(models.Officer).filter(
        models.Officer.officer_id != officer_id,
        models.Officer.user_id == officer.user_id,
        ((models.Officer.start_date <= officer.start_date) & 
         (models.Officer.end_date >= officer.start_date)) |
        ((models.Officer.start_date <= officer.end_date) & 
         (models.Officer.end_date >= officer.end_date)) |
        ((models.Officer.start_date >= officer.start_date) & 
         (models.Officer.end_date <= officer.end_date))
    ).first()
    
    if overlapping_officer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already an officer during this period"
        )
    
    return crud.officer.update(db, db_obj=db_officer, obj_in=officer.dict())

@router.delete("/{officer_id}", response_model=schemas.OfficerRead)
def delete_officer(officer_id: int, db: Session = Depends(get_db)):
    """Delete an officer."""
    officer = crud.officer.get(db, officer_id)
    if not officer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Officer not found"
        )
    
    # Check if officer has associated events or media
    if officer.events_created or officer.uploaded_media:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete officer with associated events or media"
        )
    
    return crud.officer.remove(db, obj_id=officer_id)