"""
Officers:
    - officer_id | int auto-increment primary key
    - user_id | int not null
    - role_id | int not null
    - start_date | date not null
    - end_date | date not null
    - officer_image | mediumblob not null
"""

from fastapi import APIRouter, Depends, HTTPException, status