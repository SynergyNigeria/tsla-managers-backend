import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application


def load_env_file():
    env_path = Path(__file__).resolve().parent.parent / "env"

    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value


load_env_file()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tsa_manager.settings")

application = get_wsgi_application()
