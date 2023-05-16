from dataclasses import dataclass

from fastapi import Request as _Request

from src.core import Core


@dataclass(slots=True)
class User:
    id: int
    admin: bool


class State:
    core: Core
    user: User


class Request(_Request):
    state: State  # type: ignore
