"""
Opponents:
    - opponent_id | int auto-increment primary key
    - opponent_name | varchar(255) not null
    - game_id | int not null
    - school | varchar(255) not null
    - logo | mediumblob not null
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session