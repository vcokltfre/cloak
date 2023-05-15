from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

from src.database import connect

app = FastAPI(
    title="Cloak",
    docs_url="/",
)


@app.on_event("startup")
async def startup_event() -> None:
    await connect()
