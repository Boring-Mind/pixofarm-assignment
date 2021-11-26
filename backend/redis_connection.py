import aioredis

from settings import Settings

redis_connection_pool = aioredis.ConnectionPool.from_url(
    Settings.REDIS_URL, max_connections=Settings.REDIS_MAX_CONNECTIONS
)
