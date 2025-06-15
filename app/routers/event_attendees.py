"""
EventAttendees:
    - event_id | int not null
    - user_id | int not null
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas, models, crud
from ..deps import get_db