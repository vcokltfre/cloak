from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

from src.database import connect

from .channels import router as channels_router
from .messages import router as messages_router
from .nodes import router as nodes_router
from .users import router as users_router

app = FastAPI(
    title="Cloak",
    docs_url="/",
)

app.include_router(channels_router)
app.include_router(messages_router)
app.include_router(nodes_router)
app.include_router(users_router)


@app.on_event("startup")
async def startup_event() -> None:
    await connect()
