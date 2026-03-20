from aiogram.fsm.state import State, StatesGroup


class ZodiacSignsCompatibility(StatesGroup):
    female_sign = State()
    male_sign = State()


class SubscribeToHoroscope(StatesGroup):
    selected_sign = State()
