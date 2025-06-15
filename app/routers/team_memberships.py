"""
TeamMemberships:
    - team_id | int not null foreign key
    - membership_id | int not null foreign key
    - start_date | datetime not null
    - end_date | datetime nullable
    - player_image | mediumblob nullable
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models, crud
from ..deps import get_db

router = APIRouter()

@router.post("/", response_model=schemas.TeamMembershipRead, status_code=status.HTTP_201_CREATED)
def create_team_membership(team_membership: schemas.TeamMembershipCreate, db: Session = Depends(get_db)):
    """Create a new team membership."""
    # Check if team exists
    team = crud.team.get(db, team_membership.team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    
    # Check if membership exists
    membership = crud.membership.get(db, team_membership.membership_id)
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found"
        )
    
    # Check for overlapping team memberships
    existing_membership = db.query(models.TeamMembership).filter(
        models.TeamMembership.team_id == team_membership.team_id,
        models.TeamMembership.membership_id == team_membership.membership_id,
        models.TeamMembership.start_date <= team_membership.end_date,
        models.TeamMembership.end_date >= team_membership.start_date
    ).first()
    
    if existing_membership:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Team membership already exists for this period"
        )
    
    return crud.team_membership.create(db, obj_in=team_membership)

@router.get("/team/{team_id}", response_model=List[schemas.TeamMembershipRead])
def list_team_members(
    team_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all members of a specific team."""
    # Check if team exists
    team = crud.team.get(db, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    
    return db.query(models.TeamMembership).filter(
        models.TeamMembership.team_id == team_id
    ).offset(skip).limit(limit).all()

@router.get("/membership/{membership_id}", response_model=List[schemas.TeamMembershipRead])
def list_membership_teams(
    membership_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all teams for a specific membership."""
    # Check if membership exists
    membership = crud.membership.get(db, membership_id)
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found"
        )
    
    return db.query(models.TeamMembership).filter(
        models.TeamMembership.membership_id == membership_id
    ).offset(skip).limit(limit).all()

@router.put("/{team_id}/{membership_id}", response_model=schemas.TeamMembershipRead)
def update_team_membership(
    team_id: int,
    membership_id: int,
    team_membership: schemas.TeamMembershipCreate,
    db: Session = Depends(get_db)
):
    """Update a team membership."""
    db_team_membership = db.query(models.TeamMembership).filter(
        models.TeamMembership.team_id == team_id,
        models.TeamMembership.membership_id == membership_id
    ).first()
    
    if not db_team_membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team membership not found"
        )
    
    # Check for overlapping team memberships
    existing_membership = db.query(models.TeamMembership).filter(
        models.TeamMembership.team_id == team_membership.team_id,
        models.TeamMembership.membership_id == team_membership.membership_id,
        models.TeamMembership.team_id != team_id,
        models.TeamMembership.membership_id != membership_id,
        models.TeamMembership.start_date <= team_membership.end_date,
        models.TeamMembership.end_date >= team_membership.start_date
    ).first()
    
    if existing_membership:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Team membership already exists for this period"
        )
    
    return crud.team_membership.update(
        db,
        db_obj=db_team_membership,
        obj_in=team_membership.dict()
    )

@router.delete("/{team_id}/{membership_id}", response_model=schemas.TeamMembershipRead)
def delete_team_membership(team_id: int, membership_id: int, db: Session = Depends(get_db)):
    """Delete a team membership."""
    team_membership = db.query(models.TeamMembership).filter(
        models.TeamMembership.team_id == team_id,
        models.TeamMembership.membership_id == membership_id
    ).first()
    
    if not team_membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team membership not found"
        )
    
    db.delete(team_membership)
    db.commit()
    return team_membership
