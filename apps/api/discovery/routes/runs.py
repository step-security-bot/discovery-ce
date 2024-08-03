from typing import Generator

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from fastapi_pagination import Page
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.exceptions import ValidationError as TortoiseValidationError

from discovery.db.models import Run
from discovery.db.repositories.runs import FilterableColumns, Repository
from discovery.utils import custom_generate_unique_id
from discovery.ws.runs import RunsWebSocket

router = APIRouter(
    prefix="/runs", generate_unique_id_function=custom_generate_unique_id
)
Model = pydantic_model_creator(Run)


def get_repository() -> Generator[Repository, any, any]:
    """
    Dependency to provide a database repository instance.

    Yields:
        Repository: An instance of the repository for database operations.
    """
    repo = Repository()
    try:
        yield repo
    finally:
        del repo


@router.get(
    "",
    response_model=Page[Model],
    description="Retrieve all runs with pagination. Results are paginated based on the creation date.",  # noqa: E501
    summary="Get All Runs",
    tags=["Runs"],
    responses={
        200: {"description": "Successfully retrieved the paginated list of runs."},
        500: {"description": "Internal server error."},
    },
)
async def all(
    repository: Repository = Depends(get_repository),  # noqa: B008
) -> Page[Run]:
    """
    Retrieve all runs with pagination.

    Args:
        repository (Repository): Dependency that provides a repository instance.

    Returns:
        Page[Run]: Paginated list of runs.
    """
    try:
        return await repository.paginate()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server Error"
        ) from None


@router.post(
    "/filters",
    response_model=Page[Model],
    description="Filter runs based on the provided filter criteria.",
    summary="Filter Runs",
    tags=["Runs"],
    responses={
        200: {
            "description": "Successfully retrieved the paginated list of filtered runs."
        },
        400: {"description": "Bad request due to invalid filter criteria."},
        500: {"description": "Internal server error."},
    },
)
async def filter(
    filters: FilterableColumns,
    repository: Repository = Depends(get_repository),  # noqa: B008
) -> Page[Run]:
    """
    Filter runs based on specified criteria.

    Args:
        filters (FilterableColumns): Filter criteria for querying runs.
        repository (Repository): Dependency that provides a repository instance.

    Returns:
        Page[Run]: Paginated list of filtered runs.
    """
    try:
        return await repository.filter_by(**filters)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server Error"
        ) from None


@router.get(
    "/{run_id}",
    response_model=Model,
    tags=["Runs"],
    description="Get a single run by its id. If the id is not found, a 404 response is returned.",  # noqa: E501
    summary="Get Run by ID",
    responses={
        200: {"description": "Successfully retrieved the run."},
        400: {"description": "Invalid run id. Please provide a valid run id."},
        404: {"description": "Run not found. Please provide a valid run id."},
        500: {"description": "Server error."},
    },
)
async def get_by_id(
    run_id: str,
    repository: Repository = Depends(get_repository),  # noqa: B008
) -> Run:
    try:
        run = await repository.get_by_id(run_id)
        if run is None:
            raise repository.ItemNotFoundError
        return run
    except repository.ItemNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Run not found. Please provide a valid run id.",
        ) from None
    except TortoiseValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid run id. Please provide a valid run id.",
        ) from None
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server Error"
        ) from None


manager = RunsWebSocket()


@router.websocket("/ws")
async def runs_ws(websocket: WebSocket) -> None:
    await manager.connect(websocket)
    try:
        while True:
            await manager.process(websocket)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
