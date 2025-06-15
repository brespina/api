"""
Roles:
    - role_id | int auto-increment primary key
    - role_name | varchar(30) not null unique
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models, crud
from ..deps import get_db

router = APIRouter()

@router.post("/", response_model=schemas.RoleRead, status_code=status.HTTP_201_CREATED)
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    """Create a new role."""
    # Check if role name is unique
    existing_role = db.query(models.Role).filter(
        models.Role.role_name == role.role_name
    ).first()
    
    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role with this name already exists"
        )
    
    return crud.role.create(db, obj_in=role)

@router.get("/{role_id}", response_model=schemas.RoleRead)
def read_role(role_id: int, db: Session = Depends(get_db)):
    """Get a specific role by ID."""
    role = crud.role.get(db, role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    return role

@router.get("/", response_model=List[schemas.RoleRead])
def list_roles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all roles."""
    return crud.role.get_multi(db, skip=skip, limit=limit)

@router.put("/{role_id}", response_model=schemas.RoleRead)
def update_role(
    role_id: int,
    role: schemas.RoleCreate,
    db: Session = Depends(get_db)
):
    """Update a role."""
    db_role = crud.role.get(db, role_id)
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    
    # Check if role name is unique
    existing_role = db.query(models.Role).filter(
        models.Role.role_id != role_id,
        models.Role.role_name == role.role_name
    ).first()
    
    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role with this name already exists"
        )
    
    return crud.role.update(db, db_obj=db_role, obj_in=role.dict())

@router.delete("/{role_id}", response_model=schemas.RoleRead)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    """Delete a role."""
    role = crud.role.get(db, role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    
    # Check if role has associated officers
    if role.officers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete role with associated officers"
        )
    
    return crud.role.remove(db, obj_id=role_id)