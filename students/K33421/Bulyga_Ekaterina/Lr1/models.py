from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class TimetableWeek(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    date_start: datetime
    date_end: datetime
    days: List["TimetableDay"] = Relationship(back_populates="week")


class TimetableDayDefault(SQLModel):
    date: datetime
    week_id: Optional[int] = Field(default=None, foreign_key="timetableweek.id")


class TimetableDayWeek(TimetableDayDefault):
    week: Optional[TimetableWeek] = None


class TimetableDay(TimetableDayDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    week: Optional[TimetableWeek] = Relationship(back_populates="days")
    tasks: List["Task"] = Relationship(back_populates="day")


class Notification(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    datetime: datetime
    tasks: List["Task"] = Relationship(back_populates="notification")


class TaskDefault(SQLModel):
    title: str
    description: str
    day_id: Optional[int] = Field(default=None, foreign_key="timetableday.id")
    time_start: datetime
    planned_time_end: datetime
    time_end: datetime | None
    priority: int
    notification_id: Optional[int] = Field(default=None, foreign_key="notification.id")


class TaskDayNotification(TaskDefault):
    day: Optional[TimetableDay] = None
    notification: Optional[List[Notification]] = None


class Task(TaskDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    day: Optional[TimetableDay] = Relationship(back_populates="tasks")
    notification: Optional[List[Notification]] | None = Relationship(back_populates="tasks")
