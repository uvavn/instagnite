from pydantic import ValidationError

from app.models.notifications import MessageStructure, NotificationStructure
from app.core.logger import logger
from app.services.database import DatabaseOperator
from app.services.queue import QueueManager


class NotificationValidator:
    def __init__(self):
        self._db = DatabaseOperator()

    def status(self, thread_id: str) -> bool:
        status = self._db.get_status(thread_id)
        if status == "ignore":
            return False
        if not status:
            self._db.create_user(thread_id)
            logger.info(f"Created new user in DB: {thread_id}")
        return True

    def proceed(self, notification: dict) -> None:
        try:
            notification_model = NotificationStructure(**notification)
            username, *text = notification_model.text.split(":")
            cleaned_text = ":".join(t.lstrip() for t in text)
            message_model = MessageStructure(**{
                "text": cleaned_text,
                "thread_id": notification_model.ids.get("id"),
                "username": username
            })
            logger.info(f"New message from {username}: {cleaned_text}.")
            thread_id = message_model.thread_id

            if not self.status(thread_id):
                logger.info(f"Bot have decided to ignore messages from {username}")
                return

            QueueManager.get_instance().add_to_queue(thread_id)
        except ValidationError as e:
            logger.warning(f"Unsupported type of notification. More info: {e}")