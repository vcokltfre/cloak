# pyright: reportGeneralTypeIssues=false
# pyright: reportIncompatibleVariableOverride=false

from ormar import BigInteger, Model, String

from ..metadata import database, metadata


class Channel(Model):
    class Meta:
        tablename = "channels"
        metadata = metadata
        database = database

    id: int = BigInteger(primary_key=True, autoincrement=False)
    node_id: int = BigInteger(index=True)
    name: str = String(max_length=255)
