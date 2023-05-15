from os import environ

from databases import Database
from loguru import logger
from sqlalchemy import MetaData

database = Database(environ["DB_URI"])
metadata = MetaData()


async def connect() -> None:
    logger.info("Connecting to database...")
    await database.connect()
    logger.info("Connected to database.")
