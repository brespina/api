"""
AcademicTerms:
    - term_id | int auto-increment primary key
    - semester | varchar(20) not null
    - start_date | datetime not null
    - end_date | datetime not null
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models, crud
from ..deps import get_db

router = APIRouter()

@router.post("/", response_model=schemas.AcademicTermRead, status_code=status.HTTP_201_CREATED)
def create_academic_term(term: schemas.AcademicTermCreate, db: Session = Depends(get_db)):
    """Create a new academic term."""
    # Check if term dates overlap with existing terms
    overlapping_term = db.query(models.AcademicTerm).filter(
        ((models.AcademicTerm.start_date <= term.start_date) & (models.AcademicTerm.end_date >= term.start_date)) |
        ((models.AcademicTerm.start_date <= term.end_date) & (models.AcademicTerm.end_date >= term.end_date)) |
        ((models.AcademicTerm.start_date >= term.start_date) & (models.AcademicTerm.end_date <= term.end_date))
    ).first()
    
    if overlapping_term:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Term dates overlap with an existing term"
        )
    
    return crud.academic_term.create(db, obj_in=term)

@router.get("/{term_id}", response_model=schemas.AcademicTermRead)
def read_academic_term(term_id: int, db: Session = Depends(get_db)):
    """Get a specific academic term by ID."""
    term = crud.academic_term.get(db, term_id)
    if not term:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Academic term not found"
        )
    return term

@router.get("/", response_model=List[schemas.AcademicTermRead])
def list_academic_terms(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all academic terms."""
    return crud.academic_term.get_multi(db, skip=skip, limit=limit)

@router.put("/{term_id}", response_model=schemas.AcademicTermRead)
def update_academic_term(
    term_id: int,
    term: schemas.AcademicTermCreate,
    db: Session = Depends(get_db)
):
    """Update an academic term."""
    db_term = crud.academic_term.get(db, term_id)
    if not db_term:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Academic term not found"
        )
    
    # Check for date overlaps with other terms
    overlapping_term = db.query(models.AcademicTerm).filter(
        models.AcademicTerm.term_id != term_id,
        ((models.AcademicTerm.start_date <= term.start_date) & (models.AcademicTerm.end_date >= term.start_date)) |
        ((models.AcademicTerm.start_date <= term.end_date) & (models.AcademicTerm.end_date >= term.end_date)) |
        ((models.AcademicTerm.start_date >= term.start_date) & (models.AcademicTerm.end_date <= term.end_date))
    ).first()
    
    if overlapping_term:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Term dates overlap with an existing term"
        )
    
    return crud.academic_term.update(db, db_obj=db_term, obj_in=term.dict())

@router.delete("/{term_id}", response_model=schemas.AcademicTermRead)
def delete_academic_term(term_id: int, db: Session = Depends(get_db)):
    """Delete an academic term."""
    term = crud.academic_term.get(db, term_id)
    if not term:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Academic term not found"
        )
    
    # Check if term has associated media
    if term.media:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete term with associated media"
        )
    
    return crud.academic_term.remove(db, obj_id=term_id)