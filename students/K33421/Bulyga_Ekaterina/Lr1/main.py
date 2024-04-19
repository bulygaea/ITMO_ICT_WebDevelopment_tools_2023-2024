from fastapi import FastAPI
# from views import *
from typing import List

from typing_extensions import TypedDict
from models import *

app = FastAPI()

temp_bd = [
    {
        "id": 1,
        "title": "Подготовить презентацию",
        "description": "Сделать презентацию по теме \"Docker\"",
        "day": {
            "id": 1,
            "date": "2024-03-25",
            "week": {
                "id": 1,
                "date_start": "2024-03-25",
                "date_end": "2024-03-31"
            }
        },
        "time_start": "2024-03-25T18:00:00",
        "planned_time_end": "2024-03-25T20:00:00",
        "time_end": None,
        "priority": 1,
        "notification": None
    },
    {
        "id": 2,
        "title": "Решить задачи по SQL на LeetCode",
        "description": "Решить 10 задач в курсе по SQL на сайте LeetCode",
        "day": {
            "id": 1,
            "date": "2024-03-25",
            "week": {
                "id": 1,
                "date_start": "2024-03-25",
                "date_end": "2024-03-31"
            }
        },
        "time_start": "2024-03-25T10:00:00",
        "planned_time_end": "2024-03-25T15:00:00",
        "time_end": "2024-03-25T14:30:00",
        "priority": 1,
        "notification": [
            {
                "id": 1,
                "datetime": "2024-03-25T09:30:00"
            },
            {
                "id": 2,
                "datetime": "2024-03-25T09:45:00"
            }
        ]
    }
]


@app.get("/")
def hello():
    return "Hello, [username]!"


@app.get("/tasks_list")
def tasks_list() -> List[Task]:
    return temp_bd


@app.get("/task/{task_id}")
def tasks_get(task_id: int) -> List[Task]:
    return [task for task in temp_bd if task.get("id") == task_id]


@app.post("/task")
def tasks_create(task: Task) -> TypedDict('Response', {"status": int, "data": Task}):
    task_to_append = task.model_dump()
    temp_bd.append(task_to_append)
    return {"status": 200, "data": task}


@app.delete("/task/delete{task_id}")
def task_delete(task_id: int):
    for i, task in enumerate(temp_bd):
        if task.get("id") == task_id:
            temp_bd.pop(i)
            break
    return {"status": 201, "message": "deleted"}


@app.put("/task{task_id}")
def task_update(task_id: int, task: Task) -> List[Task]:
    for war in temp_bd:
        if war.get("id") == task_id:
            task_to_append = task.model_dump()
            temp_bd.remove(war)
            temp_bd.append(task_to_append)
    return temp_bd

