from hmac import compare_digest
from os import environ
from typing import Awaitable, Callable

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response

load_dotenv()

from src.core import Core
from src.database import connect
from src.request import User

from .channels import router as channels_router
from .messages import router as messages_router
from .nodes import router as nodes_router
from .users import router as users_router

app = FastAPI(
    title="Cloak",
    docs_url="/",
    redoc_url=None,
)

app.include_router(channels_router)
app.include_router(messages_router)
app.include_router(nodes_router)
app.include_router(users_router)

core = Core()

token = environ["ADMIN_TOKEN"]


@app.on_event("startup")
async def startup_event() -> None:
    await connect()


@app.middleware("http")
async def add_core_to_request(request: Request, call_next: Callable[..., Awaitable[Response]]) -> Response:
    request.state.core = core
    return await call_next(request)


@app.middleware("http")
async def add_user_to_request(request: Request, call_next: Callable[..., Awaitable[Response]]) -> Response:
    if request.url.path in [
        "/",
        "/openapi.json",
    ]:
        return await call_next(request)

    auth = request.headers.get("Authorization")
    if not auth:
        return Response(status_code=401)

    if compare_digest(auth, token):
        request.state.user = User(id=0, admin=True)
        return await call_next(request)

    # TODO: Regular user auth
    return Response(status_code=401)
