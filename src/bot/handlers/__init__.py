from aiogram import Router, Bot, html
from redis.asyncio import Redis
from datetime import date

from .user import router as user_router
from ..clients import HoroscopeApiClient
from ..services import get_cached_horoscope, set_cached_horoscope
from ..utils.helpers import get_sign_data

main_router = Router()

main_router.include_routers(user_router)


async def send_daily_horoscope(
    bot: Bot, redis_client: Redis, horoscope_client: HoroscopeApiClient
):
    users = await redis_client.hgetall("horoscope_subscriptions")
    for user_id, sign in users.items():
        try:
            horoscope = await get_cached_horoscope(redis_client, sign)
            if horoscope is None:
                horoscope = await horoscope_client.get_horoscope_text(sign)
                await set_cached_horoscope(redis_client, sign, horoscope)

            date_today = date.today().strftime("%d.%m.%Y")

            msg_text = (
                f"🔮 Ежедневный гороскоп (чтобы отменить подписку отправьте /subscribe)!\n\n"
                f"✨ Гороскоп на {date_today} для: {html.bold(' '.join(get_sign_data(sign)))}\n\n"
                f"{horoscope}"
            )

            await bot.send_message(chat_id=int(user_id), text=msg_text)
        except Exception:
            continue
