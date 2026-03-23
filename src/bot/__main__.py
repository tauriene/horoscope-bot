import asyncio
import logging

from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from redis.asyncio import Redis
from zoneinfo import ZoneInfo

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.clients import HoroscopeApiClient
from bot.configuration import config
from bot.handlers import main_router, send_daily_horoscope
from bot.utils.ui_commands import set_ui_commands

logging.basicConfig(
    level=config.logging_level,
    format="%(asctime)s - [%(levelname)s] - %(name)s - "
           "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
)

logging.getLogger("aiogram").setLevel(logging.WARNING)
logging.getLogger("apscheduler").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def main():
    bot = Bot(config.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    redis_client = Redis(
        host=config.redis_host,
        port=config.redis_port,
        password=config.redis_password,
        db=0,
        decode_responses=True,
    )
    storage = RedisStorage(redis_client)
    horoscope_client = HoroscopeApiClient()

    scheduler = AsyncIOScheduler(timezone=ZoneInfo("Europe/Moscow"))

    scheduler.add_job(
        send_daily_horoscope,
        trigger=CronTrigger(hour=0, minute=0),
        kwargs={
            "bot": bot,
            "redis_client": redis_client,
            "horoscope_client": horoscope_client,
        },
        id="daily_horoscope",
        replace_existing=True,
    )

    scheduler.start()

    dp = Dispatcher(storage=storage)

    dp.include_router(main_router)

    await set_ui_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await horoscope_client.connect()

    try:
        await dp.start_polling(
            bot, horoscope_client=horoscope_client, redis_client=redis_client
        )
    finally:
        await bot.session.close()
        await redis_client.close()
        await horoscope_client.close()
        scheduler.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
