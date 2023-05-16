from fastapi import APIRouter, HTTPException

from src.core import Exists, NotFound
from src.request import Request

from .models import CreateUserRequest, UpdateUserRequest, User

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=User,
    responses={
        403: {"description": "You are not an admin"},
        409: {"description": "User already exists"},
    },
)
async def create_user(request: Request, body: CreateUserRequest) -> User:
    """Create a new user.

    This endpoint is admin only.
    """

    if not request.state.user.admin:
        raise HTTPException(status_code=403, detail="You are not an admin")

    try:
        user = await request.state.core.create_user(body.name, body.password)
    except Exists:
        raise HTTPException(status_code=409, detail="User already exists")

    return User(id=user.id, name=user.name)


@router.patch(
    "/{user_id}",
    response_model=User,
    responses={
        403: {"description": "You are not an admin"},
        404: {"description": "User not found"},
        409: {"description": "User already exists"},
    },
)
async def update_user(request: Request, user_id: int, body: UpdateUserRequest) -> User:
    """Update a user.

    This endpoint is admin only.
    """

    if not request.state.user.admin:
        raise HTTPException(status_code=403, detail="You are not an admin")

    try:
        user = await request.state.core.update_user(user_id, body.name)
    except NotFound:
        raise HTTPException(status_code=404, detail="User not found")
    except Exists:
        raise HTTPException(status_code=409, detail="User already exists")

    return User(id=user.id, name=user.name)


@router.delete(
    "/{user_id}",
    responses={
        403: {"description": "You are not an admin"},
        404: {"description": "User not found"},
    },
)
async def delete_user(request: Request, user_id: int) -> None:
    """Delete a user.

    This endpoint is admin only.
    """

    if not request.state.user.admin:
        raise HTTPException(status_code=403, detail="You are not an admin")

    try:
        await request.state.core.delete_user(user_id)
    except NotFound:
        raise HTTPException(status_code=404, detail="User not found")


@router.get(
    "/{user_id}",
    response_model=User,
    responses={
        404: {"description": "User not found"},
    },
)
async def get_user(request: Request, user_id: int) -> User:
    """Get a user."""

    try:
        user = await request.state.core.get_user(user_id)
    except NotFound:
        raise HTTPException(status_code=404, detail="User not found")

    return User(id=user.id, name=user.name)
