from redis.asyncio import Redis

from bot.settings import settings


def create_connection():
    """создание сессии Redis"""
    return Redis(
        host=settings.REDIS_HOST,
        db=settings.REDIS_DB,
        decode_responses=True
    )


redis_pool = create_connection()