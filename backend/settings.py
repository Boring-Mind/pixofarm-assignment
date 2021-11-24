from typing import Final


class Settings:
    DATABASE_URL: Final[str] = "sqlite+aiosqlite:///./db.sqlite3"
