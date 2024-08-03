from typing import Any

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from discovery.core.celery import celery
from discovery.runs.registry import registry
from discovery.runs.run import RunResult
from discovery.utils import custom_generate_unique_id

router = APIRouter(
    prefix="/tasks", generate_unique_id_function=custom_generate_unique_id
)


class TaskRequest(BaseModel):
    task: str
    params: dict[str, Any]

    class Config:
        arbitrary_types_allowed = True


@router.get(
    "",
    response_model=list[str],
    tags=["Tasks"],
    description="Get a list of available tasks.",
    summary="Get Available Tasks",
    responses={
        200: {"description": "Successfully retrieved the list of available tasks."},
    },
)
async def available_tasks() -> list[str]:
    """
    Retrieve a list of available tasks.

    Returns:
        list[str]: A list of available task names.
    """
    return registry.tasks


@router.post(
    "",
    response_model=RunResult,
    tags=["Tasks"],
    description="Run a specified task with provided parameters.",
    summary="Run Task",
    responses={
        200: {"description": "Successfully run the task."},
        404: {"description": "Task not found."},
    },
)
async def run_task(request: TaskRequest) -> RunResult:
    """
    Run a specified task with provided parameters.

    Args:
        request (TaskRequest): A dictionary containing the task name and parameters.

    Returns:
        RunResult: The result of the task run, including the task ID.

    Raises:
        HTTPException: If the task is not found.
    """
    task_name = request.task
    params = request.params

    if task_name in registry.tasks:
        task = celery.send_task(
            name=task_name,
            kwargs=params,
        )
        return RunResult(task.id)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found. Please provide a valid task name.",
        ) from None
