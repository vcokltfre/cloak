from fastapi import APIRouter

router = APIRouter(prefix="/channels/{channel_id}/messages", tags=["Messages"])
