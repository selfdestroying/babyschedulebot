import logging
from dataclasses import dataclass
from os import getenv

from arq.connections import RedisSettings
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", verbose=True)


@dataclass
class DataBaseConfig:
    """Database configuration."""

    url: str = getenv("SUPABASE_URL")
    key: str = getenv("SUPABASE_KEY")


@dataclass
class RedisConfig:
    """Redis connection variables."""

    db: int = int(getenv("REDIS_DATABASE", 1))
    """ Redis Database ID """
    host: str = getenv("REDIS_HOST", "redis")
    port: int = int(getenv("REDIS_PORT", 6379))
    passwd: str | None = getenv("REDIS_PASSWORD")
    username: str | None = getenv("REDIS_USERNAME")
    state_ttl: int | None = getenv("REDIS_TTL_STATE", None)
    data_ttl: int | None = getenv("REDIS_TTL_DATA", None)
    pool_settings = RedisSettings(host=host, port=port, database=db, username=username)


@dataclass
class BotConfig:
    """Bot configuration."""

    token: str = getenv("BOT_TOKEN")


@dataclass
class Configuration:
    """All in one configuration's class."""

    locale = getenv("LOCALE")
    debug = bool(getenv("DEBUG"))
    logging_level = int(getenv("LOGGING_LEVEL", logging.INFO))
    supabase = DataBaseConfig()
    redis = RedisConfig()
    bot = BotConfig()


conf = Configuration()
