import time
from collections import deque
from threading import Lock

from app.core.logger import logger
from app.services.instagram import Message


class QueueManager:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(QueueManager, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.queue = deque([])
        self.processing_now: str | None = None
        self._initialized = True

    def check_if_already_in_queue(self, thread_id: str) -> bool:
        if thread_id in self.queue or thread_id == self.processing_now:
            return False
        return True

    def start(self):
        while True:
            if self.queue:
                thread_id: str = self.queue.popleft()
                self.processing_now = thread_id
                logger.info(f"Processing message from thread {thread_id}")
                Message(int(thread_id)).proceed()
                self.processing_now = None
                logger.info(f"Finished processing thread {thread_id}")
            else:
                time.sleep(0.1)

    def add_to_queue(self, user_id: str):
        if self.check_if_already_in_queue(user_id):
            self.queue.append(user_id)
            logger.info(f"Added {user_id} to queue (queue size: {len(self.queue)})")
        else:
            logger.info(f"{user_id} already in queue or processing, skipping")

    @classmethod
    def get_instance(cls):
        return cls()