from fastapi import FastAPI, Depends, HTTPException
# from views import *
from typing import List

from sqlmodel import select
from typing_extensions import TypedDict
from models import *

# from connection import get_session

app = FastAPI()

from sqlmodel import SQLModel, Session, create_engine
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DB_ADMIN')
engine = create_engine(db_url, echo=True)


@app.on_event("startup")
def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


# temp_bd = [
#     {
#         "id": 1,
#         "title": "Подготовить презентацию",
#         "description": "Сделать презентацию по теме \"Docker\"",
#         "day_id": 1,
#         "day": {
#             "id": 1,
#             "date": "2024-03-25",
#             "week_id": 1,
#             "week": {
#                 "id": 1,
#                 "date_start": "2024-03-25",
#                 "date_end": "2024-03-31"
#             }
#         },
#         "time_start": "2024-03-25T18:00:00",
#         "planned_time_end": "2024-03-25T20:00:00",
#         "time_end": None,
#         "priority": 1,
#         "notification": None
#     },
#     {
#         "id": 2,
#         "title": "Решить задачи по SQL на LeetCode",
#         "description": "Решить 10 задач в курсе по SQL на сайте LeetCode",
#         "day_id": 1,
#         "day": {
#             "id": 1,
#             "date": "2024-03-25",
#             "week_id": 1,
#             "week": {
#                 "id": 1,
#                 "date_start": "2024-03-25",
#                 "date_end": "2024-03-31"
#             }
#         },
#         "time_start": "2024-03-25T10:00:00",
#         "planned_time_end": "2024-03-25T15:00:00",
#         "time_end": "2024-03-25T14:30:00",
#         "priority": 1,
#         "notification_id": [1, 2],
#         "notification": [
#             {
#                 "id": 1,
#                 "datetime": "2024-03-25T09:30:00"
#             },
#             {
#                 "id": 2,
#                 "datetime": "2024-03-25T09:45:00"
#             }
#         ]
#     }
# ]


@app.get("/")
def hello():
    return "Hello, [username]!"


@app.get("/tasks_list")
def tasks_list(session=Depends(get_session)) -> List[Task]:
    return session.exec(select(Task)).all()


@app.get("/task/{task_id}", response_model=TaskDayNotification)
def tasks_get(task_id: int, session=Depends(get_session)) -> Task:
    task = session.get(Task, task_id)
    return task


@app.post("/task")
def tasks_create(task: TaskDefault, session=Depends(get_session)) -> TypedDict('Response',
                                                                               {"status": int, "data": Task}):
    task = Task.model_validate(task)
    session.add(task)
    session.commit()
    session.refresh(task)
    return {"status": 200, "data": task}


@app.delete("/task/delete{task_id}")
def task_delete(task_id: int, session=Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"ok": True}


@app.patch("/task{task_id}")
def task_update(task_id: int, task: TaskDefault, session=Depends(get_session)) -> Task:
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    warrior_data = task.model_dump(exclude_unset=True)
    for key, value in warrior_data.items():
        setattr(db_task, key, value)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@app.get("/timetabledays_list")
def timetabledays_list(session=Depends(get_session)) -> List[TimetableDay]:
    return session.exec(select(TimetableDay)).all()


@app.get("/timetableday/{timetableday_id}", response_model=TimetableDayWeek)
def timetableday_get(timetableday_id: int, session=Depends(get_session)) -> TimetableDay:
    day = session.get(TimetableDay, timetableday_id)
    return day


@app.post("/timetableday")
def timetableday_create(day: TimetableDayDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                                          "data": TimetableDay}):
    day = TimetableDay.model_validate(day)
    session.add(day)
    session.commit()
    session.refresh(day)
    return {"status": 200, "data": day}


@app.get("/timetableweeks_list")
def timetableweeks_list(session=Depends(get_session)) -> List[TimetableWeek]:
    return session.exec(select(TimetableWeek)).all()


@app.get("/timetableweek/{timetableweek_id}")
def timetableweek_get(timetableweek_id: int, session=Depends(get_session)) -> TimetableWeek:
    return session.get(TimetableWeek, timetableweek_id)


@app.post("/timetableweek")
def timetableweek_create(week: TimetableWeek, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                                      "data": TimetableWeek}):
    week = TimetableWeek.model_validate(week)
    session.add(week)
    session.commit()
    session.refresh(week)
    return {"status": 200, "data": week}


@app.get("/notifications_list")
def notifications_list(session=Depends(get_session)) -> List[Notification]:
    return session.exec(select(Notification)).all()


@app.get("/notification/{notification_id}")
def notification_get(notification_id: int, session=Depends(get_session)) -> Notification:
    return session.get(Notification, notification_id)


@app.post("/notification")
def notification_create(notification: Notification, session=Depends(get_session)) -> TypedDict('Response',
                                                                                               {"status": int,
                                                                                                "data": Notification}):
    notification = Notification.model_validate(notification)
    session.add(notification)
    session.commit()
    session.refresh(notification)
    return {"status": 200, "data": notification}
