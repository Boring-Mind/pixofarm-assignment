from typing import Final


class Settings:
    DATABASE_URL: Final[str] = "sqlite+aiosqlite:///./db.sqlite3"

    # Weather settings
    # --------------------------
    WEATHER_START_DATE: Final[str] = "2020-12-01"
    WEATHER_END_DATE: Final[str] = "2020-12-08"
    WEATHER_API_ROOT: Final[str] = "http://api.weatherbit.io/v2.0/history/daily"
    WEATHER_API_KEY: Final[str] = "06ffe8e83fc343b3bfa105c32e2aa7a0"
