import json
import hashlib
import redis.asyncio as redis
from .config import REDIS_URL

redis = redis.from_url(REDIS_URL, decode_responses=True)

def generate_cache_key(base: str, params: dict) -> str:
    key = base + json.dumps(params, sort_keys=True)
    return hashlib.sha256(key.encode()).hexdigest()

async def get_from_cache(key: str):
    data = await redis.get(key)
    if data:
        return json.loads(data)
    return None

async def set_to_cache(key: str, value, expire: int = 60):
    await redis.set(key, json.dumps(value), ex=expire)