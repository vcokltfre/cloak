from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str


class CreateUserRequest(BaseModel):
    name: str
    password: str


class UpdateUserRequest(BaseModel):
    name: str
