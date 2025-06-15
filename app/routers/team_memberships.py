"""
Team Memberships is a composite key between a user and a team.
Team Memberships:
    - membership_id int FK to memberships.membership_id
    - team_id int FK to teams.team_id
    - (team_id, membership_id) is the primary key
    - player_image MEDIUMBLOB
    - start_date date not null
    - end_date date

"""

from fastapi import APIRouter, Depends, HTTPException, status
