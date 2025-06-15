"""
Matches:
    - match_id | int auto-increment primary key
    - date_time | datetime not null
    - team_id | int not null
    - opponent_id | int not null
    - watch_link | varchar(255)
    - result | varchar(20)
    - game_id | int not null
"""

from fastapi import APIRouter, Depends, HTTPException, status