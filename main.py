import os
import asyncio

from redis.asyncio import Redis, ConnectionPool
from dotenv import load_dotenv
load_dotenv(".env")

REDIS_URL = os.environ["REDIS_URL"]

redis_pool = ConnectionPool.from_url(REDIS_URL)
redis = Redis(connection_pool=redis_pool)


async def main():
    print("Hello from experiment-deck!")
    count = await redis.incr("hits:global")
    print(f"incremented {count}")


async def run():
    try:
        await main()
    finally:
        await redis.aclose()
        await redis_pool.aclose()


if __name__ == "__main__":
    asyncio.run(run())
