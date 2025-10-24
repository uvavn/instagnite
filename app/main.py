import typer
import uvicorn
import threading
import os
import subprocess
from pathlib import Path
from fastapi import FastAPI

from app.api.v1 import notifications
from app.services.instagram import Login
from app.core.config import config
from app.core.logger import logger
from app.services.queue import QueueManager

ignite = typer.Typer()

app = FastAPI()
app.include_router(notifications.router, prefix="/api/v1")

MQTT: Path = Path.cwd() / "mqtt.js"


@ignite.command(help="AI-powered real-time chat.")
def chat():
    Login(config.credentials).proceed()
    logger.info("Instagram client set.")

    thread1 = threading.Thread(target=QueueManager().start, daemon=True)
    thread1.start()
    logger.info("Queue for notifications started.")

    def _run_in_thread():
        with open(os.devnull, 'w') as devnull:
            subprocess.Popen(
                ["node", str(MQTT)],
                stdout=devnull,
                stderr=devnull,
            )
    thread2 = threading.Thread(target=_run_in_thread, daemon=True)
    thread2.start()
    logger.info("MQTT server started.")
    logger.info(f"AI is based on instructions which start with: {config.ai_instructions.basic_instruction[:200]}")
    logger.info(f"AI will stop responding when: {config.ai_instructions.stop_responding_instruction[:200]}")
    logger.warning("Low trust-score accounts might not be able to receive notifications at all. Send test message.")
    uvicorn.run(app, host="127.0.0.1", port=8000)

@ignite.command(help="Test.")
def test():
    pass

def main():
    ignite()
