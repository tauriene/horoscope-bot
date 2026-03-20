from redis.asyncio import Redis
from datetime import date


async def get_cached_horoscope(redis_client: Redis, sign: str) -> str | None:
    key = f"horoscope:{sign}:{date.today().isoformat()}"

    cached = await redis_client.get(key)
    return cached


async def set_cached_horoscope(redis_client: Redis, sign: str, value: str):
    key = f"horoscope:{sign}:{date.today().isoformat()}"

    await redis_client.set(key, value, ex=86400)


async def get_cached_compatibility(
    redis_client: Redis, female_sign: str, male_sign: str
) -> str | None:
    key = f"compatibility:{female_sign}:{male_sign}:{date.today().isoformat()}"

    cached = await redis_client.get(key)
    return cached


async def set_cached_compatibility(
    redis_client: Redis, female_sign, male_sign: str, value: str
):
    key = f"compatibility:{female_sign}:{male_sign}:{date.today().isoformat()}"

    await redis_client.set(key, value, ex=86400)
