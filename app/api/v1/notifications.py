from fastapi import APIRouter, Body
from pydantic import BaseModel
from app.services.notifications import NotificationValidator

router = APIRouter()


class Notification(BaseModel):
    notification: dict  

@router.post("/notifications")
def new_notification(body: dict = Body(...)):
    clean_body = body.get('notification', body)
    return NotificationValidator().proceed(clean_body)