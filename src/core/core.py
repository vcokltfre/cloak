from hashlib import sha512
from typing import Optional
from uuid import uuid4

from asyncpg import UniqueViolationError  # type: ignore
from ormar import NoMatch

from src.database import User
from src.utils import create_id, create_jwt


class NotFound(Exception):
    pass


class Exists(Exception):
    pass


class Core:
    """Core data controller

    This class exists primarily as a layer of indirection such that in
    the future, more intelligent features such as server-side caching
    can be implemented without rewriting large parts of the user-facing
    API code.
    """

    def __init__(self) -> None:
        pass

    def hash(self, password: str, salt: str) -> str:
        """Hash a password with 1024 rounds of sha512

        Args:
            password (str): The password to hash
            salt (str): The salt to use

        Returns:
            str: The hashed password
        """

        result = password + salt

        for _ in range(1024):
            result = sha512(result.encode()).hexdigest()

        return result

    async def create_user(self, name: str, password: str) -> User:
        """Create a new user

        Args:
            name (str): The user's name
            password (str): The user's password

        Returns:
            User: The newly created user
        """

        id = create_id()
        salt = uuid4().hex

        salt = salt[:8] + "-" + salt[8:12] + "-" + salt[12:16] + "-" + salt[16:20] + "-" + salt[20:]

        try:
            user = await User.objects.create(
                id=id,
                name=name,
                password_hash=self.hash(password, salt),
                password_salt=salt,
            )
        except UniqueViolationError:
            raise Exists

        return user

    async def get_user(self, id: int) -> User:
        """Get a user by ID

        Args:
            id (int): The user's ID

        Returns:
            User: The user
        """

        try:
            user = await User.objects.get(id=id)
        except NoMatch:
            raise NotFound

        return user

    async def update_user(self, id: int, name: str) -> User:
        """Update a user's name

        Args:
            id (int): The user's ID
            name (str): The user's new name

        Returns:
            User: The updated user
        """

        try:
            user = await User.objects.get(id=id)
        except NoMatch:
            raise NotFound

        user.name = name
        try:
            await user.save()
        except UniqueViolationError:
            raise Exists

        return user

    async def delete_user(self, id: int) -> None:
        """Delete a user

        Args:
            id (int): The user's ID
        """

        try:
            user = await User.objects.get(id=id)
        except NoMatch:
            raise NotFound

        await user.delete()

    async def login_user(self, name: str, password: str) -> Optional[str]:
        """Create a user access token

        Args:
            name (str): The user's name
            password (str): The user's password

        Returns:
            str: The user's access token
        """

        try:
            user = await User.objects.get(name=name)
        except NoMatch:
            return None

        if user.password_hash != self.hash(password, user.password_salt):
            return None

        return create_jwt(user.id)
