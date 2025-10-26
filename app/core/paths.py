from pathlib import Path

mqtt_file: Path = Path.cwd() / "mqtt.js"
credentials_file: Path = Path.cwd() / "credentials.json"

ai_instructions_folder: Path = Path.cwd() / "ai_instructions"
stop_responding_instructions_file = ai_instructions_folder / "stop_responding.txt"
basic_instructions_file = ai_instructions_folder / "basic.txt"

database_file = Path.cwd() / "targets.db"