import os

__all__ = [
    "DEBUG", "SECRET_KEY", "TUVERMIND_REDIS_HOST", "TUVERMIND_REDIS_PORT"
]

DEBUG = bool(os.getenv("TUVERMIND_DEBUG"))
SECRET_KEY = os.getenv("TUVERMIND_SECRET_KEY", None)
TUVERMIND_REDIS_HOST = os.getenv("TUVERMIND_REDIS_HOST")
TUVERMIND_REDIS_PORT = int(os.getenv("TUVERMIND_REDIS_HOST", 6379))

DB_USER = os.getenv("TUVERMIND_DB_USER")
DB_PASSWORD = os.getenv("TUVERMIND_DB_PASSWORD")
DB_HOST = os.getenv("TUVERMIND_DB_HOST")
DB_PORT = os.getenv("TUVERMIND_DB_PORT", 5432)
API_KEY = os.getenv("TUVERMIND_API_KEY")
