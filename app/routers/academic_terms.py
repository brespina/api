"""
AcademicTerms:
    - term_id | int auto-increment primary key
    - semester | varchar(20) not null
    - start_date | date not null
    - end_date | date not null
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session