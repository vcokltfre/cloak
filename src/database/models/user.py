# pyright: reportGeneralTypeIssues=false
# pyright: reportIncompatibleVariableOverride=false

from ormar import BigInteger, Model, String

from ..metadata import database, metadata


class User(Model):
    class Meta:
        tablename = "users"
        metadata = metadata
        database = database

    id: int = BigInteger(primary_key=True, autoincrement=False)
    name: str = String(min_length=2, max_length=32, index=True, unique=True)

    password_hash: str = String(min_length=128, max_length=128)  # SHA512 hash
    password_salt: str = String(min_length=36, max_length=36)  # UUID4
