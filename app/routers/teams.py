"""
Teams are the main entities in the system.
Teams:
    - team_id | int auto-increment primary key
    - game_id | int FK to games.game_id
    - team_name | varchar(255) not null
    - created_at | date not null
    - achievements | varchar(255)
    - coordinator_id | int FK to coordinators.coordinator_id
    - wins | int
    - losses | int
"""

from fastapi import APIRouter, Depends, HTTPException, status