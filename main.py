import os
import asyncio

from redis.asyncio import Redis, ConnectionPool
from redis.exceptions import RedisError
from dotenv import load_dotenv
load_dotenv(".env")

REDIS_URL = os.environ["REDIS_URL"]

redis_pool = ConnectionPool.from_url(REDIS_URL)
redis = Redis(connection_pool=redis_pool)


async def main():
    print("Hello from experiment-deck!")
    try:
        count = await redis.incr("hits:global")
    except RedisError as exc:
        print(f"Increment failed: {exc}")
        return
    print(f"incremented {count}")


async def run():
    try:
        await main()
    finally:
        await redis.aclose()
        await redis_pool.aclose()


if __name__ == "__main__":
    asyncio.run(run())
