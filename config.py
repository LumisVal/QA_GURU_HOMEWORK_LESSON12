import os
from dotenv import load_dotenv

load_dotenv()


def to_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.lower() in ("1", "true", "yes", "y", "on")


BASE_URL = os.getenv("BASE_URL", "https://demoqa.com")
SELENOID_URL = os.getenv("SELENOID_URL", "selenoid.autotests.cloud/wd/hub")

LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")

BROWSER_NAME = os.getenv("BROWSER_NAME", "chrome")
BROWSER_VERSION = os.getenv("BROWSER_VERSION", "")
HEADLESS = to_bool(os.getenv("HEADLESS"), False)
WINDOW_SIZE = os.getenv("WINDOW_SIZE", "1920x1080")