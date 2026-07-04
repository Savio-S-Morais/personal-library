import os
from pathlib import Path

from app import create_app

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env.development"

if ENV_FILE.exists():
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key, value)

app = create_app()

if __name__ == "__main__":
    app.run()