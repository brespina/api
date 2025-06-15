"""
Roles:
    - role_id | int auto-increment primary key
    - role_name | varchar(255) not null
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session