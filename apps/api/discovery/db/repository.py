from typing import Any, Dict, Generic, List, Optional, TypeVar, Unpack

from fastapi_pagination.ext.tortoise import paginate
from tortoise import Model as TortoiseModel
from tortoise.expressions import Q

Model = TypeVar("Model", bound=TortoiseModel)
Columns = TypeVar("Columns")
FilterableColumns = TypeVar("FilterableColumns")


class Repository(Generic[Model, Columns, FilterableColumns]):
    def __init__(self, model: type[Model]) -> None:
        self.__model = model

    async def get_by_id(self, _id: str) -> Optional[Model]:
        """Get an object from the data store by its ID.

        Args:
            _id (str): The ID of the object to retrieve.

        Returns:
            Optional[Model]: The retrieved object or None if not found.
        """
        return await self.model.filter(id=_id).first()

    async def get_all(self, order_by: Optional[Columns] = None) -> List[Model]:
        """Get all objects from the data store.

        Args:
            order_by (Optional[Columns]): The column to order the results by.

        Returns:
            List[Model]: A list of all objects in the data store.
        """
        query = self.model.all()
        if order_by:
            query = query.order_by(order_by)
        return await query

    async def paginate(self, order_by: Optional[str] = None) -> Any:
        """Paginate the results from the data store.

        Args:
            order_by (Optional[str]): The column to order the results by.

        Returns:
            Any: Paginated results.
        """
        if order_by:
            return await paginate(self.model, order_by)
        return await paginate(self.model)

    async def create(self, **item: Dict[str, Any]) -> None:
        """Create a new object in the data store.

        Args:
            item (Dict[str, Any]): The object to create.

        Returns:
            None
        """
        await self.model.create(**item)

    async def update(self, _id: str, **item: Dict[str, Any]) -> None:
        """Update an existing object in the data store.

        Args:
            _id (str): The ID of the object to update.
            item (Dict[str, Any]): The object to update.

        Returns:
            None
        """
        await self.model.filter(id=_id).update(**item)

    async def delete(self, _id: str) -> None:
        """Delete an object from the data store.

        Args:
            _id (str): The ID of the object to delete.

        Returns:
            None
        """
        await self.model.filter(id=_id).delete()

    def generate_expressions(
        self, join_type: str = "AND", **filterable_columns: Unpack[FilterableColumns]
    ) -> Q:
        """Generate Tortoise Query expressions based on the provided filterable columns.

        Args:
            join_type (str, optional): The type of join to use when combining the
            generated expressions. Defaults to "AND".
            **filterable_columns: The filterable columns to generate expressions for.
            Each key-value pair represents a column name and its corresponding value.

        Returns:
            Q: A Tortoise Query expression.
        """
        q_objects = [
            Q(**{key: value})
            for key, value in filterable_columns.items()
            if value is not None
        ]
        return Q(*q_objects, join_type=join_type)

    @property
    def model(self) -> type[Model]:
        return self.__model

    class ItemNotFoundError(Exception):
        def __init__(self) -> None:
            self.message = "Item not found."
            super().__init__(self.message)
