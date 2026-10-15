
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field


app = FastAPI(
    title="TaskFlow API",
    description="A task management API for AWS ECS deployment practice",
    version="1.0.0",
)


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(default="", max_length=500)
    priority: Priority = Priority.medium


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    priority: Optional[Priority] = None
    task_status: Optional[TaskStatus] = None


class Task(TaskCreate):
    id: int
    task_status: TaskStatus = TaskStatus.pending
    created_at: datetime


tasks: dict[int, Task] = {}
next_id = 1


@app.get("/")
def home():
    return {
        "message": "Welcome to TaskFlow API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    global next_id

    task = Task(
        id=next_id,
        **payload.model_dump(),
        task_status=TaskStatus.pending,
        created_at=datetime.now(timezone.utc),
    )

    tasks[next_id] = task
    next_id += 1

    return task


@app.get("/tasks")
def list_tasks(
    task_status: Optional[TaskStatus] = None,
    priority: Optional[Priority] = None,
    search: Optional[str] = Query(default=None, max_length=100),
):
    result = list(tasks.values())

    if task_status:
        result = [t for t in result if t.task_status == task_status]

    if priority:
        result = [t for t in result if t.priority == priority]

    if search:
        term = search.casefold()
        result = [
            t for t in result
            if term in t.title.casefold()
            or term in t.description.casefold()
        ]

    return {"count": len(result), "tasks": result}


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = tasks.get(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@app.patch("/tasks/{task_id}")
def update_task(task_id: int, payload: TaskUpdate):
    task = tasks.get(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    updates = payload.model_dump(exclude_unset=True)
    updated = task.model_copy(update=updates)

    tasks[task_id] = updated
    return updated


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    del tasks[task_id]

    return {"message": "Task deleted successfully", "id": task_id}


@app.get("/stats")
def task_statistics():
    total = len(tasks)

    return {
        "total_tasks": total,
        "pending": sum(t.task_status == TaskStatus.pending for t in tasks.values()),
        "in_progress": sum(t.task_status == TaskStatus.in_progress for t in tasks.values()),
        "completed": sum(t.task_status == TaskStatus.completed for t in tasks.values()),
        "high_priority": sum(t.priority == Priority.high for t in tasks.values()),
    }
