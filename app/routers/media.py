"""
Media:
    - media_id | int auto-increment primary key
    - media_image | mediumblob not null
    - academic_term_id | int not null
    - uploaded_by_officer_id | int not null
    - date_uploaded | date not null
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session