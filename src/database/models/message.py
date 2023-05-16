# pyright: reportGeneralTypeIssues=false
# pyright: reportIncompatibleVariableOverride=false

from ormar import BigInteger, Model, String

from ..metadata import database, metadata


class Message(Model):
    class Meta:
        tablename = "messages"
        metadata = metadata
        database = database

    id: int = BigInteger(primary_key=True, autoincrement=False)
    channel_id: int = BigInteger(index=True)
    author_id: int = BigInteger(index=True)
    content: str = String(max_length=4096)
