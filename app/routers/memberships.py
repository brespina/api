"""
Memberships:
    - membership_id | int auto-increment primary key
    - user_id | int not null foreign key
    - start_date | datetime not null
    - end_date | datetime not null
    - shirt_size_id | int nullable foreign key
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models, crud
from ..deps import get_db

router = APIRouter()

@router.post("/", response_model=schemas.MembershipRead, status_code=status.HTTP_201_CREATED)
def create_membership(membership: schemas.MembershipCreate, db: Session = Depends(get_db)):
    """Create a new membership."""
    # Check if user exists
    user = crud.user.get(db, membership.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if shirt size exists if provided
    if membership.shirt_size_id:
        shirt_size = crud.shirt_size.get(db, membership.shirt_size_id)
        if not shirt_size:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shirt size not found"
            )
    
    # Check for overlapping memberships
    overlapping_membership = db.query(models.Membership).filter(
        models.Membership.user_id == membership.user_id,
        ((models.Membership.start_date <= membership.start_date) & 
         (models.Membership.end_date >= membership.start_date)) |
        ((models.Membership.start_date <= membership.end_date) & 
         (models.Membership.end_date >= membership.end_date)) |
        ((models.Membership.start_date >= membership.start_date) & 
         (models.Membership.end_date <= membership.end_date))
    ).first()
    
    if overlapping_membership:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has an active membership during this period"
        )
    
    return crud.membership.create(db, obj_in=membership)

@router.get("/{membership_id}", response_model=schemas.MembershipRead)
def read_membership(membership_id: int, db: Session = Depends(get_db)):
    """Get a specific membership by ID."""
    membership = crud.membership.get(db, membership_id)
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found"
        )
    return membership

@router.get("/", response_model=List[schemas.MembershipRead])
def list_memberships(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all memberships."""
    return crud.membership.get_multi(db, skip=skip, limit=limit)

@router.get("/user/{user_id}", response_model=List[schemas.MembershipRead])
def list_user_memberships(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all memberships for a specific user."""
    # Check if user exists
    user = crud.user.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return db.query(models.Membership).filter(
        models.Membership.user_id == user_id
    ).offset(skip).limit(limit).all()

@router.put("/{membership_id}", response_model=schemas.MembershipRead)
def update_membership(
    membership_id: int,
    membership: schemas.MembershipCreate,
    db: Session = Depends(get_db)
):
    """Update a membership."""
    db_membership = crud.membership.get(db, membership_id)
    if not db_membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found"
        )
    
    # Check if shirt size exists if provided
    if membership.shirt_size_id:
        shirt_size = crud.shirt_size.get(db, membership.shirt_size_id)
        if not shirt_size:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shirt size not found"
            )
    
    # Check for overlapping memberships
    overlapping_membership = db.query(models.Membership).filter(
        models.Membership.membership_id != membership_id,
        models.Membership.user_id == membership.user_id,
        ((models.Membership.start_date <= membership.start_date) & 
         (models.Membership.end_date >= membership.start_date)) |
        ((models.Membership.start_date <= membership.end_date) & 
         (models.Membership.end_date >= membership.end_date)) |
        ((models.Membership.start_date >= membership.start_date) & 
         (models.Membership.end_date <= membership.end_date))
    ).first()
    
    if overlapping_membership:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has an active membership during this period"
        )
    
    return crud.membership.update(db, db_obj=db_membership, obj_in=membership.dict())

@router.delete("/{membership_id}", response_model=schemas.MembershipRead)
def delete_membership(membership_id: int, db: Session = Depends(get_db)):
    """Delete a membership."""
    membership = crud.membership.get(db, membership_id)
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found"
        )
    
    # Check if membership has associated team memberships
    if membership.team_memberships:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete membership with associated team memberships"
        )
    
    return crud.membership.remove(db, obj_id=membership_id)