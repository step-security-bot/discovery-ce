from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Response
from fastapi_pagination import add_pagination
from tortoise.contrib.fastapi import RegisterTortoise

from discovery.routes import runs, tasks


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    from discovery.core import config

    async with RegisterTortoise(
        app,
        db_url=config.database_url,
        modules={"models": ["discovery.db.models"]},
        generate_schemas=True,
    ):
        yield


app: FastAPI = FastAPI(title="Discovery", version="1.0.0", lifespan=lifespan)

add_pagination(app)


@app.get("/health")
async def check_health() -> Response:
    return Response(status_code=200, content="OK")


app.include_router(runs.router)
app.include_router(tasks.router)
