"""
Games:
    - game_id | int auto-increment primary key
    - game_name | varchar(255) not null
    - bg_image | mediumblob not null
"""


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas, models, crud
from ..deps import get_db

router = APIRouter()


@router.post("/", response_model=schemas.GameRead, status_code=status.HTTP_201_CREATED)
def create_game(game_in: schemas.GameCreate, db: Session = Depends(get_db)):
    if db.query(models.Game).filter(models.Game.game_name == game_in.game_name).first():
        raise HTTPException(status_code=400, detail="Game already registered")

    return crud.game.create(db, obj_in=game_in)


@router.get("/{game_id}", response_model=schemas.GameRead)
def read_game(game_id: int, db: Session = Depends(get_db)):
    db_game = crud.game.get(db, game_id)
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")
    return db_game


@router.get("/", response_model=list[schemas.GameRead])
def list_games(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.game.get_multi(db, skip=skip, limit=limit)


@router.delete("/{game_id}", response_model=schemas.GameRead)
def delete_game(game_id: int, db: Session = Depends(get_db)):
    return crud.game.remove(db, obj_id=game_id)
