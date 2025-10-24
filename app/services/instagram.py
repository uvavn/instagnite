import pyotp
from typing import Callable, Any
from pydantic import ValidationError
from functools import wraps
from instagrapi import Client
from instagrapi.exceptions import UnknownError, BadPassword, ChallengeRequired, LoginRequired, ClientNotFoundError
from instagrapi.types import DirectMessage

from app.core.logger import logger
from app.models.ai import AIRespond
from app.models.config import Credentials
from app.models.instagram import Conversation
from app.services.database import DatabaseOperator
from app.services.files import save_credentials
from app.services.ai import ai_respond

cl = Client()
cl.delay_range = [3, 7]


class InstagramError(Exception):
    pass


def instagrapi_method(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except (UnknownError, BadPassword, ChallengeRequired, LoginRequired, ClientNotFoundError) as e:
            e = type(e).__name__
            raise InstagramError(e)
    return wrapper


class Login:
    def __init__(self, credentials: Credentials):
        self.credentials = credentials

    @instagrapi_method
    def _via_credentials(self) -> None:
        if self.credentials.two_factor:
            cl.login(username=self.credentials.username, password=self.credentials.password,
                     verification_code=pyotp.TOTP(self.credentials.two_factor).now())
        else:
            cl.login(username=self.credentials.username, password=self.credentials.password)
        self.credentials.session = cl.get_settings()

    @instagrapi_method
    def _via_session(self) -> None:
        cl.set_settings(self.credentials.session)
        cl.get_timeline_feed()

    def proceed(self):
        if self.credentials.session:
            try:
                self._via_session()
                return
            except InstagramError as e:
                logger.warning(f"Session invalid: {e}. Retrying...")
        try:
            self._via_credentials()
        except InstagramError as e:
            logger.error(f"Something went wrong during Instagram login by credentials: {e}")
            exit(1)
        save_credentials(self.credentials)


class Message:
    def __init__(self, thread_id: int):
        self._thread_id = thread_id
        self._db = DatabaseOperator()

    @instagrapi_method
    def read(self) -> list[Conversation]:
        thread: list[DirectMessage] = cl.direct_messages(thread_id=self._thread_id)

        def safe_validate(msg):
            try:
                return Conversation.model_validate(msg.model_dump())
            except ValidationError as e:
                logger.debug(f"Skipped invalid msg in thread {self._thread_id}: {e}")
                return None

        validated_messages = [safe_validate(message) for message in thread]
        conversation = [msg for msg in validated_messages if msg is not None]
        return conversation

    @instagrapi_method
    def respond(self, respond: str):
        cl.direct_send(text=respond, thread_ids=[self._thread_id])

    def proceed(self) -> None:
        try:
            thread = self.read()
            full_respond: AIRespond = ai_respond(thread)
            if not len(full_respond.ai_respond) == 0:
                self.respond(full_respond.ai_respond)
            logger.info(f"Bot set {self._thread_id} status on {full_respond.status} and responded: {full_respond.ai_respond}")
            self._db.update_status(str(self._thread_id), full_respond.status)
        except InstagramError as e:
            logger.critical("Something went wrong during Instagram API operations. Consider closing program for"
                            "safety. "
                            f"More info: {e}")

