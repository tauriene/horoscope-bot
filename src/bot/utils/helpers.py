from bot.utils.constans import ZODIAC_SIGNS_LITERALS


def get_sign_data(sign: str) -> str:
    return ZODIAC_SIGNS_LITERALS[sign]
