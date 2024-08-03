from typing import Literal, NotRequired, TypedDict, Unpack

from fastapi_pagination.ext.tortoise import paginate

from ..models import Run
from ..models import RunStatus as Status
from ..repository import Repository as BaseRepository


class FilterableColumns(TypedDict):
    status: Status
    owner_id: NotRequired[str] = None
    parent_id: NotRequired[str] = None


class Repository(
    BaseRepository[
        Run,
        Literal[
            "id",
            "parameters",
            "status",
            "result",
            "started_at",
            "failed_at",
            "completed_at",
            "owner_id",
            "created_at",
            "updated_at",
            "parent_id",
        ],
        FilterableColumns,
    ],
):
    def __init__(self) -> None:
        super().__init__(Run)

    async def filter_by(
        self,
        **filters: Unpack[FilterableColumns],
    ) -> list[Run]:
        expressions = self.generate_expressions(join_type="AND", **filters)

        return await paginate(self.model.filter(expressions).all())
