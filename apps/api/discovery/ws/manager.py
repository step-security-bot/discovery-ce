from enum import Enum
from typing import Any, Generic, TypeVar

from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

Data = TypeVar("Data")


class AvailableActions(str, Enum):
    QUERY: str = "QUERY"


class BaseMessage(BaseModel):
    action: AvailableActions
    data: dict[str, Any]


class GenericMessage(BaseMessage, Generic[Data]):
    data: Data

    class Config:
        arbitrary_types_allowed = True


class GenericResponse(BaseModel):
    success: bool = True
    data: Any

    class Config:
        arbitrary_types_allowed = True


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket) -> None:
        await websocket.close()
        self.active_connections.remove(websocket)

    @staticmethod
    async def respond(to: WebSocket, **kwargs: dict[str, any]) -> None:
        if "success" in kwargs:
            success = kwargs.pop("success")
        response = jsonable_encoder(
            {
                "data": kwargs,
                "success": success,
            }
        )

        await to.send_json(response)
