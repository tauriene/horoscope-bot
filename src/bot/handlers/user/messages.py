from aiogram import Router, html
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from redis.asyncio import Redis

from bot.handlers.user.states import ZodiacSignsCompatibility
from bot.keyboards.inline import (
    get_inline_signs_keyboard,
    schedule_subscribe_kb,
    schedule_unsubscribe_kb,
)

msg_router = Router()


@msg_router.message(CommandStart())
async def start_msg(msg: Message):
    await msg.answer(
        "🔮 Добро пожаловать в мир звёзд и тайн!\n"
        "Я помогу тебе узнать, что приготовила судьба на сегодня "
        "и насколько подходят знаки зодиака походят друг другу.\n\n"
        f"{html.bold('Выбирай, с чего начнём:')}\n"
        "/horoscope — гороскоп на сегодня\n"
        "/compatibility — совместимость знаков\n"
        "/subscribe — настроить ежедневный гороскоп"
    )


@msg_router.message(Command("horoscope"))
async def horoscope_msg(msg: Message):
    await msg.answer(
        "✨ Давай заглянем в будущее...\n\nВыбери знак зодиака 👇",
        reply_markup=get_inline_signs_keyboard(),
    )


@msg_router.message(Command("subscribe"))
async def schedule_cmd(msg: Message, redis_client: Redis):
    user = await redis_client.hget("horoscope_subscriptions", str(msg.from_user.id))

    if user is None:
        await msg.answer(
            "🤔 Хотите получать гороскоп на день в 00:00 (UTC+3)?",
            reply_markup=schedule_subscribe_kb,
        )
    else:
        await msg.answer(
            "😢 Хотите отписаться от ежедневного гороскопа?",
            reply_markup=schedule_unsubscribe_kb,
        )


@msg_router.message(Command("compatibility"))
async def compatibility_msg(msg: Message, state: FSMContext):
    await msg.answer(
        "💞 Проверим, что говорят звёзды о вашей паре...\n\n"
        "👩 1) Сначала выбери знак зодиака женщины 👇",
        reply_markup=get_inline_signs_keyboard(),
    )
    await state.set_state(ZodiacSignsCompatibility.female_sign)
