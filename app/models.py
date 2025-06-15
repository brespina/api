from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, Boolean, Enum, Text, LargeBinary, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum


class ShirtSizeEnum(enum.Enum):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    signup_date = Column(Date, nullable=False)
    paid_dues = Column(Boolean)
    phone_number = Column(String(20), nullable=True)
    discord_username = Column(String(100), nullable=True)
    profile_picture = Column(LargeBinary, nullable=True)

    # relationships
    officers = relationship("Officer", back_populates="user")
    memberships = relationship("Membership", back_populates="user")
    event_attendees = relationship("EventAttendee", back_populates="user")
    coordinators = relationship("Coordinator", back_populates="user")


class Role(Base):
    __tablename__ = "roles"
    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(30), unique=True, nullable=False)

    officers = relationship("Officer", back_populates="role")


class Officer(Base):
    __tablename__ = "officers"
    officer_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    officer_image = Column(LargeBinary, nullable=True)

    # relationships
    user = relationship("User", back_populates="officers")
    role = relationship("Role", back_populates="officers")
    events_created = relationship("Event", back_populates="created_by_officer_id")
    uploaded_media = relationship("Media", back_populates="uploaded_by")

    # constraints
    __table_args__ = (
        CheckConstraint('end_date is null or end_date > start_date', name='chk_dates'),
    )


class Coordinator(Base):
    __tablename__ = "coordinators"
    coordinator_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.game_id"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)

    # relationships
    user = relationship("User", back_populates="coordinator_roles")
    game = relationship("Game", back_populates="coordinators")

    # constraints
    __table_args__ = (
        CheckConstraint('end_date is null or end_date > start_date', name='chk_coord_dates_end_after_start'),
    )


class Membership(Base):
    __tablename__ = "memberships"
    membership_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    start_date = Column(DateTime, server_default=func.now(), nullable=True)
    end_date = Column(DateTime, nullable=False)
    shirt_size_id = Column(Integer, ForeignKey("shirt_sizes.size_id"), nullable=True)

    # relationships
    user = relationship("User", back_populates="memberships")
    shirt_size = relationship("ShirtSize", back_populates="memberships")
    team_memberships = relationship("TeamMembership", back_populates="memberships")

    # constraints
    __table_args__ = (
        CheckConstraint('end_date > start_date', name='chk_end_after_start'),
    )


class ShirtSize(Base):
    __tablename__ = "shirt_sizes"
    size_id = Column(Integer, primary_key=True, index=True)
    size_name = Column(Enum(ShirtSizeEnum), nullable=True)
    
    # relationships
    memberships = relationship("Membership", back_populates="shirt_size")


class Event(Base):
    __tablename__ = "events"
    event_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(300), nullable=False)
    date_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    attendance = Column(Integer) 
    created_by_officer_id = Column(Integer, ForeignKey("officers.officer_id"), nullable=False)

    # relationships
    created_by_officer = relationship("Officer", back_populates="events_created")
    attendees = relationship("EventAttendee", back_populates="event")

    # constraints
    __table_args__ = (
        CheckConstraint('end_time > date_time', name='chk_end_after_start'),
    )


class EventAttendee(Base):
    __tablename__ = "event_attendees"
    event_id = Column(Integer, ForeignKey("events.event_id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    
    # relationships
    event = relationship("Event", back_populates="attendees")
    user = relationship("User", back_populates="event_attendees")


class Game(Base):
    __tablename__ = "games"
    game_id = Column(Integer, primary_key=True, index=True)
    game_name = Column(String(100), unique=True, nullable=False)

    # relationships
    teams = relationship("Team", back_populates="game")
    coordinators = relationship("Coordinator", back_populates="game")
    opponents = relationship("Opponent", back_populates="game")
    matches = relationship("Match", back_populates="game")


class Match(Base):
    __tablename__ = "matches"
    match_id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime, nullable=False)
    team_id = Column(Integer, ForeignKey("teams.team_id", ondelete="CASCADE"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.game_id"), nullable=False)
    opponent_id = Column(Integer, ForeignKey("opponents.opponent_id"), nullable=False)
    bg_image = Column(LargeBinary)
    watch_link = Column(String(255))
    result = Column(String(100))

    # relationships
    team = relationship("Team", back_populates="matches")
    opponent = relationship("Opponent", back_populates="matches")
    game = relationship("Game", back_populates="matches")

    
class Opponent(Base):
    __tablename__ = "opponents"
    opponent_id = Column(Integer, primary_key=True, index=True)
    opponent_name = Column(String(100), nullable=False)
    game_id = Column(Integer, ForeignKey("games.game_id"), nullable=False)
    school = Column(String(100), nullable=False)
    logo = Column(LargeBinary, nullable=True)
    


class Media(Base):
    __tablename__ = "media"
    media_id = Column(Integer, primary_key=True, index=True)
    media_image = Column(LargeBinary, nullable=True)
    academic_term_id = Column(Integer, ForeignKey("academic_terms.term_id"), nullable=False)
    uploaded_by_officer_id = Column(Integer, ForeignKey("officers.officer_id"), nullable=False)
    date_uploaded = Column(Date, nullable=False)

    # relationships
    academic_term = relationship("AcademicTerm", back_populates="media")
    uploaded_by = relationship("Officer", back_populates="uploaded_media")


class Sponsor(Base):
    __tablename__ = "sponsors"
    sponsor_id = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    sponsor_name = Column(String(100), nullable=False)
    sponsor_logo = Column(LargeBinary)


class TeamMembership(Base):
    __tablename__ = "team_memberships"
    team_id = Column(Integer, ForeignKey("teams.team_id", ondelete="CASCADE"), primary_key=True)
    membership_id = Column(Integer, ForeignKey("memberships.membership_id", ondelete="CASCADE"), primary_key=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)

    # relationships
    team = relationship("Team", back_populates="team_memberships")
    membership = relationship("Membership", back_populates="team_memberships")
    user = relationship("User", back_populates="team_memberships")


class Team(Base):
    __tablename__ = "teams"
    team_id = Column(Integer, primary_key=True, index=True)
    team_name = Column(String(100), unique=True, nullable=False)
    game_id = Column(Integer, ForeignKey("games.game_id"), nullable=False)
    team_logo = Column(LargeBinary, nullable=True)
    created_at = Column(DateTime, nullable=False)
    
    # relationships
    game = relationship("Game", back_populates="teams")
    matches = relationship("Match", back_populates="team")
    team_memberships = relationship("TeamMembership", back_populates="team")
    
