import logging
from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv

load_dotenv()


@dataclass
class DataBaseConfig:
    """Database configuration."""

    url: str = getenv("SUPABASE_URL")
    key: str = getenv("SUPABASE_KEY")


@dataclass
class BotConfig:
    """Bot configuration."""

    token: str = getenv("BOT_TOKEN")


@dataclass
class Configuration:
    """All in one configuration's class."""

    locale = "ru_RU.UTF-8"
    debug = bool(getenv("DEBUG"))
    logging_level = int(getenv("LOGGING_LEVEL", logging.INFO))
    supabase = DataBaseConfig()
    bot = BotConfig()


conf = Configuration()
