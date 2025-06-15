from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class AcademicTermBase(BaseModel):
    semester: str
    start_date: datetime
    end_date: datetime


class AcademicTermCreate(AcademicTermBase):
    pass


class AcademicTermRead(AcademicTermBase):
    term_id: int

    class Config:
        orm_mode = True


class CoordinatorBase(BaseModel):
    user_id: int
    game_id: int
    start_date: datetime
    end_date: Optional[datetime] = None


class CoordinatorCreate(CoordinatorBase):
    pass


class CoordinatorRead(CoordinatorBase):
    coordinator_id: int

    class Config:
        orm_mode = True


class EventAttendeeBase(BaseModel):
    user_id: int
    event_id: int


class EventAttendeeCreate(EventAttendeeBase):
    pass


class EventAttendeeRead(EventAttendeeBase):
    user_id: int
    event_id: int

    class Config:
        orm_mode = True


class EventBase(BaseModel):
    title: str
    description: str
    location: str
    date_time: datetime
    end_time: datetime
    attendence: Optional[int] = None
    created_by_officer_id: int


class EventCreate(EventBase):
    pass


class EventRead(EventBase):
    event_id: int

    class Config:
        orm_mode = True


class GameBase(BaseModel):
    game_name: str
    bg_image: Optional[bytes] = None


class GameCreate(GameBase):
    pass


class GameRead(GameBase):
    game_id: int

    class Config:
        orm_mode = True


class MatchBase(BaseModel):
    team_id: int
    opponent_id: int
    date_time: datetime
    watch_link: Optional[str] = None
    result: Optional[str] = None
    game_id: int


class MatchCreate(MatchBase):
    pass


class MatchRead(MatchBase):
    match_id: int

    class Config:
        orm_mode = True


class MediaBase(BaseModel):
    media_image: Optional[bytes] = None
    academic_term_id: int
    uploaded_by_officer_id: int
    date_uploaded: datetime


class MediaCreate(MediaBase):
    pass


class MediaRead(MediaBase):
    media_id: int

    class Config:
        orm_mode = True


class MembershipBase(BaseModel):
    user_id: int
    start_date: Optional[datetime] = None
    end_date: datetime
    shirt_size_id: Optional[int] = None


class MembershipCreate(MembershipBase):
    pass


class MembershipRead(MembershipBase):
    membership_id: int

    class Config:
        orm_mode = True


class OfficerBase(BaseModel):
    user_id: int
    role_id: int
    start_date: datetime
    end_date: Optional[datetime] = None
    officer_image: Optional[bytes] = None


class OfficerCreate(OfficerBase):
    pass


class OfficerRead(OfficerBase):
    officer_id: int

    class Config:
        orm_mode = True


class OpponentBase(BaseModel):
    opponent_name: str
    game_id: int
    school: Optional[str] = None
    logo: Optional[bytes] = None


class OpponentCreate(OpponentBase):
    pass


class OpponentRead(OpponentBase):
    opponent_id: int

    class Config:
        orm_mode = True


class RoleBase(BaseModel):
    role_name: str


class RoleCreate(RoleBase):
    pass


class RoleRead(RoleBase):
    role_id: int

    class Config:
        orm_mode = True


class ShirtSizeBase(BaseModel):
    size_name: Optional[str] = None


class ShirtSizeCreate(ShirtSizeBase):
    pass


class ShirtSizeRead(ShirtSizeBase):
    size_id: int

    class Config:
        orm_mode = True


class SponsorBase(BaseModel):
    sponsor_name: str
    start_date: datetime
    end_date: Optional[datetime] = None
    sponsor_logo: Optional[bytes] = None
    sponsor_website: Optional[str] = None


class SponsorCreate(SponsorBase):
    pass


class SponsorRead(SponsorBase):
    sponsor_id: int

    class Config:
        orm_mode = True


class TeamMembershipBase(BaseModel):
    team_id: int
    membership_id: int
    player_image: Optional[bytes] = None
    start_date: datetime
    end_date: Optional[datetime] = None


class TeamMembershipCreate(TeamMembershipBase):
    pass


class TeamMembershipRead(TeamMembershipBase):
    team_id: int
    membership_id: int

    class Config:
        orm_mode = True


class TeamBase(BaseModel):
    team_name: str
    game_id: int
    coordinator_id: int
    achievements: Optional[str] = None
    wins: int
    losses: int


class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    team_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    password_hash: str
    first_name: str
    last_name: str
    signup_date: Optional[datetime] = None


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    user_id: int

    class Config:
        orm_mode = True
