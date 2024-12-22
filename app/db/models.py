from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class UserRole(Enum):
    ADMIN = "ADMIN"
    COMEDIAN = "COMEDIAN"
    HOST = "HOST"
    VIEWER = "VIEWER"


@dataclass(slots=True)
class UserModel():
    id: int
    login: str
    password: str
    email: str
    role: UserRole
    name: Optional[str] = None
    date_birth: Optional[datetime] = None
    city: Optional[str] = None


@dataclass(slots=True)
class PlaceModel():
    id: int
    name: str
    owner: Optional[str] = None
    city: Optional[str] = None


@dataclass(slots=True)
class EventModel():
    id: int
    title: str
    description: str
    created_at: datetime
    started_at: datetime


@dataclass(slots=True)
class ReviewModel():
    id: int
    content: str
    mark: int
    user: UserModel
    event: EventModel
    created_at: datetime


@dataclass(slots=True)
class RecordModel():
    id: int
    user: UserModel
    event: EventModel
    created_at: datetime
