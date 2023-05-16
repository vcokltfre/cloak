from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.request import Request


class LoginRequest(BaseModel):
    name: str
    password: str


class Token(BaseModel):
    token: str


router = APIRouter(prefix="/login", tags=["Login"])


@router.post(
    "/",
    response_model=Token,
    responses={
        401: {"description": "Invalid credentials"},
    },
)
async def login(request: Request, body: LoginRequest) -> Token:
    token = await request.state.core.login_user(body.name, body.password)

    if token is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return Token(token=token)
