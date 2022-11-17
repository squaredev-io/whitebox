import asyncio
import functools
from collections import deque

from crontab import CronTab
from src.utils.exceptions import (
    TaskNotFoundException,
    TaskAlreadyRunningException,
    TaskNotRunningException,
)
from src.utils.logger import cronLogger as logger
from src.schemas.task import (
    TaskDefinition,
    RunningTask,
    TaskLog,
    TaskInfo,
    TaskStatus,
    State,
    TaskRealTimeInfo,
    EventType,
)
from typing import Callable, Optional, Coroutine, List, Dict, Deque

from functools import lru_cache
import datetime

import pytz


def now():
    return datetime.datetime.utcnow().replace(tzinfo=pytz.utc)


class Task_Manager:
    def __init__(self):
        self._definitions: Dict[str, TaskDefinition] = {}
        self._real_time: Dict[str, TaskRealTimeInfo] = {}
        self._running_tasks: Dict[str, RunningTask] = {}
        self._log_queue: Deque[TaskLog] = deque()

        self._is_running: bool = False
        self._is_shutting_down: bool = False

        self._cleanup_tasks: List[asyncio.Task] = []

    def clear(self):
        """Resets the"""
        if self._is_running or self._is_shutting_down:
            raise Exception("Cannot clear before shutdown")
        self._definitions: Dict[str, TaskDefinition] = {}
        self._real_time: Dict[str, TaskRealTimeInfo] = {}
        self._running_tasks: Dict[str, RunningTask] = {}
        self._log_queue: Deque[TaskLog] = deque()

    def register(
        self,
        async_callable: Callable[[], Coroutine],
        crontab: str = None,
        name: str = None,
    ):
        name = name or async_callable.__name__
        if name in self._definitions:
            raise Exception(f"Task <{name}> already exists.")

        definition = TaskDefinition(
            name=name, async_callable=async_callable, crontab=crontab, enabled=True
        )
        self._definitions[name] = definition
        self._real_time[name] = TaskRealTimeInfo(
            name=name, status="registered", next_run_ts=None
        )

        self._log_event("task_registered", definition.name)

    def _log_event(self, event_type: EventType, task_name: str, error: str = None):
        self._log_queue.append(
            TaskLog(
                event_type=event_type,
                task_name=task_name,
                crontab=self._definitions[task_name].crontab,
                enabled=self._definitions[task_name].enabled,
                error=error,
            )
        )

    def _get_task_definition(self, name: str) -> TaskDefinition:
        try:
            return self._definitions[name]
        except KeyError as e:
            raise TaskNotFoundException from e

    def _get_running_task(self, name: str) -> RunningTask:
        try:
            return self._running_tasks[name]
        except KeyError as e:
            raise TaskNotRunningException from e

    def _is_task_running(self, name: str) -> bool:
        return name in self._running_tasks

    def get_task_info(self, name: str) -> TaskInfo:
        definition = self._get_task_definition(name)
        return TaskInfo(
            name=definition.name,
            enabled=definition.enabled,
            crontab=definition.crontab,
            started_at=self._get_task_started_at(name),
            stopped_at=self._get_task_stopped_at(name),
            next_run_in=self._get_task_next_run_in(name),
            previous_status=self._get_previous_status(name) or "registered",
            status=self._get_task_status(name),
        )

    # TODO: Implement functionality
    def _get_task_started_at(self, name: str):
        rt_info = self._real_time.get(name)
        if not rt_info:
            raise TaskNotFoundException("task not found")
        return rt_info.started_at

    # TODO: Implement functionality
    def _get_task_stopped_at(self, name: str):
        rt_info = self._real_time.get(name)
        if not rt_info:
            raise TaskNotFoundException("task not found")
        return rt_info.stopped_at

    def _get_task_status(self, name: str) -> TaskStatus:
        rt_info = self._real_time.get(name)
        if not rt_info:
            raise TaskNotFoundException("task not found")
        return rt_info.status

    def _get_previous_status(self, name: str) -> TaskStatus:
        rt_info = self._real_time.get(name)
        if not rt_info:
            raise TaskNotFoundException("task not found")
        return rt_info.previous_status

    def _get_task_next_run_in(self, name: str) -> Optional[int]:
        definition = self._get_task_definition(name)
        if definition.crontab is None:
            return None
        return CronTab(definition.crontab).next(default_utc=True)

    def _create_running_task(self, definition: TaskDefinition) -> RunningTask:
        running_task = RunningTask(
            task_definition=definition,
            asyncio_task=asyncio.get_event_loop().create_task(
                definition.async_callable()
            ),
            since=now().timestamp(),
        )
        running_task.asyncio_task.add_done_callback(
            functools.partial(self._on_task_done, definition.name)
        )
        return running_task

    async def cancel_task(self, name: str):
        if not self._is_task_running(name):
            raise TaskNotRunningException("task not running")
        logger.info(f"Cancelling {name}")
        self._get_task_definition(name)
        running_task = self._get_running_task(name)
        cancelled = running_task.asyncio_task.cancel()
        return cancelled

    def run_task(self, name: str) -> None:
        if self._is_task_running(name):
            raise TaskAlreadyRunningException("task already running")

        definition = self._get_task_definition(name)
        running_task = self._create_running_task(definition)
        self._running_tasks[definition.name] = running_task

        self._real_time[name] = TaskRealTimeInfo(
            name=name,
            status="running",
            previous_status=self._get_previous_status(name),
            started_at=now().timestamp(),
            next_run_ts=now().timestamp() + (self._get_task_next_run_in(name) or 0),
        )

    # TODO: Implement disable task functionality
    def disable_task(self, name: str):
        return False

    # TODO: Implement enable task functionality
    def enable_task(self, name: str):
        return False

    def get_all_tasks_info(self) -> List[TaskInfo]:
        return [self.get_task_info(name) for name in self._definitions.keys()]

    def _on_task_done(self, task_name: str, task: asyncio.Task) -> None:
        definition = self._get_task_definition(task_name)
        del self._running_tasks[task_name]

        try:
            exception = task.exception()
        except asyncio.CancelledError:
            self._log_event("task_cancelled", definition.name)

            self._real_time[task_name] = TaskRealTimeInfo(
                name=task_name,
                status="pending",
                previous_status="cancelled",
                next_run_ts=None,
                started_at=self._get_task_started_at(task_name),
                stopped_at=now().timestamp(),
            )
            task = asyncio.get_event_loop().create_task(
                self.on_task_cancelled(task_name)
            )
            self._cleanup_tasks.append(task)
            return

        if exception:
            self._log_event("task_failed", definition.name, error=str(exception))

            self._real_time[task_name] = TaskRealTimeInfo(
                name=task_name,
                status="pending",
                previous_status="failed",
                next_run_ts=None,
                started_at=self._get_task_started_at(task_name),
                stopped_at=now().timestamp(),
            )
            task = asyncio.get_event_loop().create_task(
                self.on_task_exception(task_name, exception)
            )
            self._cleanup_tasks.append(task)
            return

        self._log_event("task_finished", definition.name)

        self._real_time[task_name] = TaskRealTimeInfo(
            name=task_name,
            status="pending",
            previous_status="finished",
            started_at=self._get_task_started_at(task_name),
            stopped_at=now().timestamp(),
            next_run_ts=now().timestamp() + self._get_task_next_run_in(task_name)
            if definition.crontab
            else None,
        )
        task = asyncio.get_event_loop().create_task(self.on_task_finished(task_name))
        self._cleanup_tasks.append(task)
        return

    async def _on_task_started(self, task_name: str):
        definition = self._get_task_definition(task_name)

        self._log_event("task_started", definition.name)
        await self.on_task_started(task_name)

    async def run(self, state: State = None):
        if self._is_running:
            logger.warning("Ignoring current calling of run(). Already running.")
            return

        self._is_running = True
        await self.on_startup()

        if state:
            for task_info in state.tasks_info:
                if task_info.name in self._definitions:
                    self._definitions[task_info.name].crontab = task_info.crontab
                    self._definitions[task_info.name].enabled = task_info.enabled

                    self._real_time[task_info.name].status = task_info.status

        await self._run_ad_infinitum()

    async def _run_ad_infinitum(self):
        while True and self._is_running:
            for task_name, rt_info in self._real_time.items():
                this_time_ts = now().timestamp()

                if rt_info.status == "registered":
                    delta: int = self._get_task_next_run_in(task_name) or 0

                    self._real_time[task_name] = TaskRealTimeInfo(
                        name=task_name,
                        status="pending",
                        previous_status="registered",
                        next_run_ts=now().timestamp() + delta,
                    )
                elif (
                    not self._is_shutting_down
                    and rt_info.status in ["pending", "finished"]
                    and rt_info.next_run_ts is not None
                    and rt_info.next_run_ts <= this_time_ts
                ):
                    self.run_task(task_name)
                elif rt_info.status == "running" and not self._is_task_running(
                    task_name
                ):
                    self.run_task(task_name)
                else:  # rt_info.status in ["cancelled", "failed"]:
                    ...
            await asyncio.sleep(1.5)

    async def shutdown(self):
        await asyncio.sleep(2)
        logger.info("Shutting down...")
        logger.info(f"Cancelling {len(self._running_tasks)} running tasks...")
        self._is_shutting_down = True

        for running_task in self._running_tasks.values():
            await self.cancel_task(running_task.task_definition.name)
            logger.debug(f"Cancelled task {running_task.task_definition.name}")

        await asyncio.gather(*self._cleanup_tasks)
        logger.debug("Cleanup tasks finished.")

        await self.on_shutdown()

        self._is_running = False
        self._is_shutting_down = False

    async def on_task_started(self, task_name: str):

        ...

    async def on_task_exception(self, task_name: str, exception: BaseException):
        ...

    async def on_task_cancelled(self, task_name: str):
        logger.info(f"Cancelled {task_name}")

    async def on_task_finished(self, task_name: str):
        logger.info(f"Finished {task_name}")

    async def on_startup(self):
        ...

    async def on_shutdown(self):
        ...

    def state(self) -> State:
        state = State(created_at=now(), tasks_info=self.get_all_tasks_info())
        return state


@lru_cache()
def get_task_manager():
    return Task_Manager()
