"""
ShirtSizes:
    - size_id | int auto-increment primary key
    - size_name | enum('XS', 'S', 'M', 'L', 'XL', 'XXL') nullable
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models, crud
from ..deps import get_db

router = APIRouter()

@router.post("/", response_model=schemas.ShirtSizeRead, status_code=status.HTTP_201_CREATED)
def create_shirt_size(shirt_size: schemas.ShirtSizeCreate, db: Session = Depends(get_db)):
    """Create a new shirt size."""
    # Check if size name is unique
    if shirt_size.size_name:
        existing_size = db.query(models.ShirtSize).filter(
            models.ShirtSize.size_name == shirt_size.size_name
        ).first()
        
        if existing_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Shirt size with this name already exists"
            )
    
    return crud.shirt_size.create(db, obj_in=shirt_size)

@router.get("/{size_id}", response_model=schemas.ShirtSizeRead)
def read_shirt_size(size_id: int, db: Session = Depends(get_db)):
    """Get a specific shirt size by ID."""
    shirt_size = crud.shirt_size.get(db, size_id)
    if not shirt_size:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shirt size not found"
        )
    return shirt_size

@router.get("/", response_model=List[schemas.ShirtSizeRead])
def list_shirt_sizes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all shirt sizes."""
    return crud.shirt_size.get_multi(db, skip=skip, limit=limit)

@router.put("/{size_id}", response_model=schemas.ShirtSizeRead)
def update_shirt_size(
    size_id: int,
    shirt_size: schemas.ShirtSizeCreate,
    db: Session = Depends(get_db)
):
    """Update a shirt size."""
    db_shirt_size = crud.shirt_size.get(db, size_id)
    if not db_shirt_size:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shirt size not found"
        )
    
    # Check if size name is unique
    if shirt_size.size_name:
        existing_size = db.query(models.ShirtSize).filter(
            models.ShirtSize.size_id != size_id,
            models.ShirtSize.size_name == shirt_size.size_name
        ).first()
        
        if existing_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Shirt size with this name already exists"
            )
    
    return crud.shirt_size.update(db, db_obj=db_shirt_size, obj_in=shirt_size.dict())

@router.delete("/{size_id}", response_model=schemas.ShirtSizeRead)
def delete_shirt_size(size_id: int, db: Session = Depends(get_db)):
    """Delete a shirt size."""
    shirt_size = crud.shirt_size.get(db, size_id)
    if not shirt_size:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shirt size not found"
        )
    
    # Check if shirt size has associated memberships
    if shirt_size.memberships:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete shirt size with associated memberships"
        )
    
    return crud.shirt_size.remove(db, obj_id=size_id)