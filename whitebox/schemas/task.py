import datetime
from asyncio.tasks import Task
from dataclasses import dataclass

from pydantic import BaseModel, Field
from typing import Callable, Coroutine, Optional, List, Dict, Deque, Literal
from uuid import UUID, uuid4
import datetime

import pytz


def now():
    return datetime.datetime.utcnow().replace(tzinfo=pytz.utc)


TaskStatus = Literal[
    "registered", "running", "finished", "pending", "cancelled", "failed"
]

EventType = Literal[
    "task_registered",
    "task_started",
    "task_failed",
    "task_finished",
    "task_cancelled",
    "task_disabled",
]


class TaskInfo(BaseModel):
    uid: UUID = uuid4()
    name: str
    status: str
    previous_status: str
    enabled: bool
    crontab: str = None
    created_at: datetime.datetime = now().timestamp()
    started_at: datetime.datetime = None
    stopped_at: datetime.datetime = None
    next_run_in: int = None


class TaskDefinition(BaseModel):
    name: str
    async_callable: Callable[[], Coroutine]
    enabled: bool = True
    crontab: Optional[str] = None


@dataclass
class RunningTask:
    task_definition: TaskDefinition
    asyncio_task: Task
    since: datetime.datetime


class TaskLog(BaseModel):
    event_type: EventType
    task_name: str
    crontab: str = None
    enabled: bool
    error: str = None
    timestamp: int = Field(default_factory=lambda: datetime.datetime.now().timestamp())


class State(BaseModel):
    created_at: datetime.datetime
    tasks_info: List[TaskInfo]


class TaskRealTimeInfo(BaseModel):
    name: str
    status: TaskStatus
    previous_status: Optional[TaskStatus]
    next_run_ts: Optional[int]
    started_at: Optional[datetime.datetime]
    stopped_at: Optional[datetime.datetime]
