import json

from aiogram import Router, F, html
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from datetime import date

from redis.asyncio import Redis

from bot.handlers.user.states import SubscribeToHoroscope, ZodiacSignsCompatibility
from bot.keyboards.inline import get_inline_signs_keyboard
from bot.clients import HoroscopeApiClient
from bot.utils.constans import ZODIAC_SIGNS_LITERALS
from bot.utils.helpers import get_sign_data
from bot.services import (
    get_cached_horoscope,
    set_cached_horoscope,
    get_cached_compatibility,
    set_cached_compatibility,
)

cb_router = Router()


@cb_router.callback_query(StateFilter(None), F.data.in_(ZODIAC_SIGNS_LITERALS))
async def horoscope_cb(
    cb: CallbackQuery, horoscope_client: HoroscopeApiClient, redis_client: Redis
):
    horoscope = await get_cached_horoscope(redis_client, cb.data)
    if horoscope is None:
        horoscope = await horoscope_client.get_horoscope_text(cb.data)
        await set_cached_horoscope(redis_client, cb.data, horoscope)

    date_today = date.today().strftime("%d.%m.%Y")

    msg_text = (
        f"✨ Гороскоп на {date_today} для: {html.bold(' '.join(get_sign_data(cb.data)))}\n\n"
        f"{horoscope}"
    )

    await cb.answer()
    await cb.message.edit_text(msg_text)


@cb_router.callback_query(F.data == "subscribe_horoscope")
async def subscribe_horoscope_cb(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await cb.message.edit_text(
        "Выберите свой знак зодиака 👇", reply_markup=get_inline_signs_keyboard()
    )
    await state.set_state(SubscribeToHoroscope.selected_sign)


@cb_router.callback_query(F.data == "unsubscribe_horoscope")
async def unsubscribe_horoscope_cb(cb: CallbackQuery, redis_client: Redis):
    await redis_client.hdel("horoscope_subscriptions", str(cb.from_user.id))

    await cb.answer()
    await cb.message.edit_text("😔 Вы отписались от рассылки")


@cb_router.callback_query(
    SubscribeToHoroscope.selected_sign, F.data.in_(ZODIAC_SIGNS_LITERALS)
)
async def selected_sign_cb(
    cb: CallbackQuery,
    state: FSMContext,
    redis_client: Redis,
):
    await state.clear()
    await redis_client.hset("horoscope_subscriptions", str(cb.from_user.id), cb.data)

    await cb.answer()
    await cb.message.edit_text("❤️ Вы подписались на ежедневный гороскоп!")


@cb_router.callback_query(
    ZodiacSignsCompatibility.female_sign, F.data.in_(ZODIAC_SIGNS_LITERALS)
)
async def female_sign_cb(cb: CallbackQuery, state: FSMContext):
    await state.update_data(female_sign=cb.data)

    await cb.answer()
    await cb.message.edit_text(
        "🧑 2) Теперь выбери знак зодиака мужчины 👇",
        reply_markup=get_inline_signs_keyboard(),
    )
    await state.set_state(ZodiacSignsCompatibility.male_sign)


@cb_router.callback_query(
    ZodiacSignsCompatibility.male_sign, F.data.in_(ZODIAC_SIGNS_LITERALS)
)
async def male_sign_cb(
    cb: CallbackQuery,
    state: FSMContext,
    horoscope_client: HoroscopeApiClient,
    redis_client: Redis,
):
    user_data = await state.get_data()

    female_sign = user_data["female_sign"]
    male_sign = cb.data

    await state.clear()

    compatibility = await get_cached_compatibility(redis_client, female_sign, male_sign)
    if compatibility is None:
        relationship_type, love, marriage, description = (
            await horoscope_client.get_compatibility_text(female_sign, male_sign)
        )

        data = {
            "relationship_type": relationship_type,
            "love": love,
            "marriage": marriage,
            "description": description,
        }

        await set_cached_compatibility(
            redis_client, female_sign, male_sign, json.dumps(data)
        )
    else:
        data = json.loads(compatibility)

        relationship_type = data["relationship_type"]
        love = data["love"]
        marriage = data["marriage"]
        description = data["description"]

    msg_text = (
        "✨ Совместимость по звёздам для:\n"
        f"{html.bold(' '.join(get_sign_data(female_sign)))} + {html.bold(' '.join(get_sign_data(male_sign)))}\n\n"
        f"{html.bold(f'Тип отношений: {relationship_type}')}\n\n"
        f"❤️ Совместимость в любви: {love}%\n"
        f"💍 Совместимость в браке: {marriage}%\n\n"
        f"{description}"
    )

    await cb.answer()
    await cb.message.edit_text(msg_text)
