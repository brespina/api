"""
Media:
    - media_id | int auto-increment primary key
    - media_image | mediumblob nullable
    - academic_term_id | int not null foreign key
    - uploaded_by_officer_id | int not null foreign key
    - date_uploaded | datetime not null
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models, crud
from ..deps import get_db

router = APIRouter()

@router.post("/", response_model=schemas.MediaRead, status_code=status.HTTP_201_CREATED)
def create_media(media: schemas.MediaCreate, db: Session = Depends(get_db)):
    """Create new media."""
    # Check if academic term exists
    term = crud.academic_term.get(db, media.academic_term_id)
    if not term:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Academic term not found"
        )
    
    # Check if officer exists
    officer = crud.officer.get(db, media.uploaded_by_officer_id)
    if not officer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Officer not found"
        )
    
    return crud.media.create(db, obj_in=media)

@router.get("/{media_id}", response_model=schemas.MediaRead)
def read_media(media_id: int, db: Session = Depends(get_db)):
    """Get specific media by ID."""
    media = crud.media.get(db, media_id)
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found"
        )
    return media

@router.get("/", response_model=List[schemas.MediaRead])
def list_media(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all media."""
    return crud.media.get_multi(db, skip=skip, limit=limit)

@router.get("/term/{term_id}", response_model=List[schemas.MediaRead])
def list_term_media(
    term_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all media for a specific academic term."""
    # Check if term exists
    term = crud.academic_term.get(db, term_id)
    if not term:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Academic term not found"
        )
    
    return db.query(models.Media).filter(
        models.Media.academic_term_id == term_id
    ).offset(skip).limit(limit).all()

@router.delete("/{media_id}", response_model=schemas.MediaRead)
def delete_media(media_id: int, db: Session = Depends(get_db)):
    """Delete media."""
    media = crud.media.get(db, media_id)
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found"
        )
    
    return crud.media.remove(db, obj_id=media_id)