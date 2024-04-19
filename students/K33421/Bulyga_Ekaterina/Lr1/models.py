from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class TimetableWeek(BaseModel):
    id: int
    date_start: datetime
    date_end: datetime


class TimetableDay(BaseModel):
    id: int
    date: datetime
    week: TimetableWeek


class Notification(BaseModel):
    id: int
    datetime: datetime


class Task(BaseModel):
    id: int
    title: str
    description: str
    day: TimetableDay
    time_start: datetime
    planned_time_end: datetime
    time_end: datetime | None
    priority: int
    notification: Optional[List[Notification]] | None
