from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, date

from app.db.models import UserRole


class UserCreateSchema(BaseModel):
    login: str
    password: str
    email: EmailStr
    name: Optional[str] = None
    date_birth: date
    role: UserRole
    city: str

    class Config:
        extra = 'forbid'


class UserUpdateSchema(BaseModel):
    login: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    date_birth: Optional[date] = None
    role: Optional[UserRole] = None
    city: Optional[str] = None

    class Config:
        extra = 'forbid'


# Event Schemas
class EventCreateSchema(BaseModel):
    title: str
    description: str
    place_id: int
    started_at: datetime

    class Config:
        extra = 'forbid'


class EventUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    place_id: Optional[int] = None
    started_at: Optional[datetime] = None

    class Config:
        extra = 'forbid'


# Place Schemas
class PlaceCreateSchema(BaseModel):
    name: str
    owner: Optional[str] = None
    city: Optional[str] = None

    class Config:
        extra = 'forbid'


class PlaceUpdateSchema(BaseModel):
    name: Optional[str] = None
    owner: Optional[str] = None
    city: Optional[str] = None

    class Config:
        extra = 'forbid'


# Feedback Schemas
class ReviewCreateSchema(BaseModel):
    content: str
    mark: int  # Rating from 1 to 5
    user_id: int
    event_id: int

    class Config:
        extra = 'forbid'


class ReviewUpdateSchema(BaseModel):
    content: Optional[str] = None
    mark: Optional[int] = None

    class Config:
        extra = 'forbid'


# Record Schemas
class RecordCreateSchema(BaseModel):
    user_id: int
    event_id: int

    class Config:
        extra = 'forbid'


class RecordUpdateSchema(BaseModel):
    user_id: Optional[int] = None
    event_id: Optional[int] = None

    class Config:
        extra = 'forbid'
