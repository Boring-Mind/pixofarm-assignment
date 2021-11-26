from datetime import timedelta
from typing import Final


class Settings:
    DATABASE_URL: Final[str] = "sqlite+aiosqlite:///./db.sqlite3"

    REDIS_URL: Final[str] = "redis://redis"
    REDIS_MAX_CONNECTIONS: Final[int] = 10
    CORRELATION_CACHE_KEY: Final[str] = "correlation"
    CORRELATION_CACHE_EXP: Final[timedelta] = timedelta(minutes=1)

    # Weather settings
    # --------------------------
    WEATHER_START_DATE: Final[str] = "2020-12-01"
    WEATHER_END_DATE: Final[str] = "2020-12-08"
    WEATHER_API_ROOT: Final[str] = "http://api.weatherbit.io/v2.0/history/daily"
    WEATHER_API_KEY: Final[str] = "06ffe8e83fc343b3bfa105c32e2aa7a0"
