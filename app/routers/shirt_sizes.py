"""
ShirtSizes:
    - size_id | int auto-increment primary key
    - size_name | varchar(20) not null
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session