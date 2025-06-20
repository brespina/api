from typing import Any, Dict, Generic, List, Optional, Type
from typing_extensions import TypeVar
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .database import Base
from . import models, schemas

ModelType = TypeVar("ModelType", bound=Base)  # type: ignore
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType]):
    """Generic CRUD utilities with *just* what we need right now."""

    def __init__(self, model: Type[ModelType]):
        self.model = model

    # READ -------------------------------------------------------------------
    def get(self, db: Session, obj_id: Any) -> Optional[ModelType]:
        return db.query(self.model).get(obj_id)

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    # CREATE -----------------------------------------------------------------
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # UPDATE -----------------------------------------------------------------
    def update(
        self, db: Session, *, db_obj: ModelType, obj_in: Dict[str, Any]
    ) -> ModelType:
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # DELETE -----------------------------------------------------------------
    def remove(self, db: Session, *, obj_id: int) -> ModelType:
        obj = db.query(self.model).get(obj_id)
        if obj is None:
            raise ValueError(f"Object with id {obj_id} not found")
        db.delete(obj)
        db.commit()
        return obj


# Create CRUD instances for each model
academic_term = CRUDBase[models.AcademicTerm, schemas.AcademicTermCreate](models.AcademicTerm)
coordinator = CRUDBase[models.Coordinator, schemas.CoordinatorCreate](models.Coordinator)
event_attendee = CRUDBase[models.EventAttendee, schemas.EventAttendeeCreate](models.EventAttendee)
event = CRUDBase[models.Event, schemas.EventCreate](models.Event)
game = CRUDBase[models.Game, schemas.GameCreate](models.Game)
match = CRUDBase[models.Match, schemas.MatchCreate](models.Match)
media = CRUDBase[models.Media, schemas.MediaCreate](models.Media)
membership = CRUDBase[models.Membership, schemas.MembershipCreate](models.Membership)
officer = CRUDBase[models.Officer, schemas.OfficerCreate](models.Officer)
opponent = CRUDBase[models.Opponent, schemas.OpponentCreate](models.Opponent)
role = CRUDBase[models.Role, schemas.RoleCreate](models.Role)
shirt_size = CRUDBase[models.ShirtSize, schemas.ShirtSizeCreate](models.ShirtSize)
sponsor = CRUDBase[models.Sponsor, schemas.SponsorCreate](models.Sponsor)
team_membership = CRUDBase[models.TeamMembership, schemas.TeamMembershipCreate](models.TeamMembership)
team = CRUDBase[models.Team, schemas.TeamCreate](models.Team)
user = CRUDBase[models.User, schemas.UserCreate](models.User)







