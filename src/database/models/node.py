# pyright: reportGeneralTypeIssues=false
# pyright: reportIncompatibleVariableOverride=false

from ormar import BigInteger, Model, String

from ..metadata import database, metadata


class Node(Model):
    class Meta:
        tablename = "nodes"
        metadata = metadata
        database = database

    id: int = BigInteger(primary_key=True, autoincrement=False)
    owner_id: int = BigInteger(index=True)
    name: str = String(max_length=255)
