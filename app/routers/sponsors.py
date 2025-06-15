"""
Sponsors:
    - sponsor_id | int auto-increment primary key
    - sponsor_name | varchar(100) not null
    - start_date | datetime not null
    - end_date | datetime nullable
    - sponsor_logo | mediumblob nullable
    - sponsor_website | varchar(255) nullable
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models, crud
from ..deps import get_db

router = APIRouter()

@router.post("/", response_model=schemas.SponsorRead, status_code=status.HTTP_201_CREATED)
def create_sponsor(sponsor: schemas.SponsorCreate, db: Session = Depends(get_db)):
    """Create a new sponsor."""
    # Check if sponsor name is unique
    existing_sponsor = db.query(models.Sponsor).filter(
        models.Sponsor.sponsor_name == sponsor.sponsor_name
    ).first()
    
    if existing_sponsor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sponsor with this name already exists"
        )
    
    return crud.sponsor.create(db, obj_in=sponsor)

@router.get("/{sponsor_id}", response_model=schemas.SponsorRead)
def read_sponsor(sponsor_id: int, db: Session = Depends(get_db)):
    """Get a specific sponsor by ID."""
    sponsor = crud.sponsor.get(db, sponsor_id)
    if not sponsor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sponsor not found"
        )
    return sponsor

@router.get("/", response_model=List[schemas.SponsorRead])
def list_sponsors(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all sponsors."""
    return crud.sponsor.get_multi(db, skip=skip, limit=limit)

@router.get("/active", response_model=List[schemas.SponsorRead])
def list_active_sponsors(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all active sponsors."""
    from datetime import datetime
    current_date = datetime.now()
    
    return db.query(models.Sponsor).filter(
        models.Sponsor.start_date <= current_date,
        (models.Sponsor.end_date >= current_date) | (models.Sponsor.end_date == None)
    ).offset(skip).limit(limit).all()

@router.put("/{sponsor_id}", response_model=schemas.SponsorRead)
def update_sponsor(
    sponsor_id: int,
    sponsor: schemas.SponsorCreate,
    db: Session = Depends(get_db)
):
    """Update a sponsor."""
    db_sponsor = crud.sponsor.get(db, sponsor_id)
    if not db_sponsor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sponsor not found"
        )
    
    # Check if sponsor name is unique
    existing_sponsor = db.query(models.Sponsor).filter(
        models.Sponsor.sponsor_id != sponsor_id,
        models.Sponsor.sponsor_name == sponsor.sponsor_name
    ).first()
    
    if existing_sponsor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sponsor with this name already exists"
        )
    
    return crud.sponsor.update(db, db_obj=db_sponsor, obj_in=sponsor.dict())

@router.delete("/{sponsor_id}", response_model=schemas.SponsorRead)
def delete_sponsor(sponsor_id: int, db: Session = Depends(get_db)):
    """Delete a sponsor."""
    sponsor = crud.sponsor.get(db, sponsor_id)
    if not sponsor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sponsor not found"
        )
    
    return crud.sponsor.remove(db, obj_id=sponsor_id)