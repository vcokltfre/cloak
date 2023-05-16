from fastapi import Request as _Request

from src.core import Core


class State:
    core: Core


class Request(_Request):
    state: State  # type: ignore
