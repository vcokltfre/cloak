# pyright: reportGeneralTypeIssues=false
# pyright: reportIncompatibleVariableOverride=false

from ormar import BigInteger, Model, String

from ..metadata import database, metadata


class Member(Model):
    class Meta:
        tablename = "members"
        metadata = metadata
        database = database

    id: str = String(max_length=255, primary_key=True)
    node_id: int = BigInteger(index=True)
    user_id: int = BigInteger(index=True)
