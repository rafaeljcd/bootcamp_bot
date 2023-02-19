from bot import DiscordBot
from os import environ
from dotenv import load_dotenv
from discord import VoiceClient, Intents
from pathlib import Path
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler
import logging
import re
import asyncio

env_path = Path.cwd() / ".env"
load_dotenv(dotenv_path=env_path)

# https://stackoverflow.com/a/58893367/14859274
formatter = Formatter(
    fmt='%(asctime)s - %(threadName)s - %(levelname)s - %(name)s - %(funcName)s:%(lineno)d - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


def setup_logger(
        logger_name: str,
        level: int = logging.INFO
):
    log = logging.getLogger(f"{logger_name}")
    log_file_name = f"{logger_name}_logfile.log"
    logger_dir_path = Path(__file__).parent / "files" / "logs" / f"{logger_name}"

    if not logger_dir_path.exists():
        logger_dir_path.mkdir(parents=True)
    log_file_path = logger_dir_path / log_file_name

    log_handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1, encoding='utf-8')
    log_handler.suffix = "%Y%m%d"
    log_handler.extMatch = re.compile(r"^\d{8}$")
    log_handler.setFormatter(formatter)

    log.setLevel(level)
    log.addHandler(log_handler)


info_log_name = "info"
error_log_name = "error"

setup_logger(info_log_name, logging.DEBUG)
setup_logger(error_log_name, logging.ERROR)

logger = logging.getLogger(info_log_name)
error_logger = logging.getLogger(error_log_name)

ch = logging.StreamHandler()
ch.setFormatter(formatter)
logging.getLogger('').addHandler(ch)
logging.getLogger('').setLevel(logging.INFO)

token = environ.get('token')

intents = Intents.default()
intents.invites = True

VoiceClient.warn_nacl = False

bot = DiscordBot(
    command_prefix="!",
    intents=intents
)


async def main():
    async with bot:
        await bot.start(token)


if __name__ == '__main__':
    asyncio.run(main())
