import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, Future, as_completed

import httpx


def sync_get_product(client: httpx.Client, product_id: int) -> tuple[int, dict]:
    response = client.get(f"https://dummyjson.com/products/{product_id}?delay=1000")
    return product_id, response.json()


async def async_get_product(client: httpx.AsyncClient, product_id: int) -> tuple[int, dict]:
    response = await client.get(f"https://dummyjson.com/products/{product_id}?delay=1000")
    return product_id, response.json()


def get_multi_threaded(number_of_requests, max_threads):
    client = httpx.Client(limits=httpx.Limits(max_connections=500, max_keepalive_connections=100), timeout=60.0)
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures: list[Future] = []
        for i in range(1, number_of_requests + 1):
            future = executor.submit(sync_get_product, client, i)
            futures.append(future)
        for future in as_completed(futures):
            product_id, _ = future.result()
            print(f"Completed {product_id}", end=" , ")


async def get_multi_task(number_of_requests):
    async_client = httpx.AsyncClient(limits=httpx.Limits(max_connections=500, max_keepalive_connections=100),
                                     timeout=60.0)
    coroutines = []
    for i in range(1, number_of_requests + 1):
        coroutine = async_get_product(async_client, i)
        coroutines.append(coroutine)
    for coroutine in asyncio.as_completed(coroutines):
        product_id, _ = await coroutine
        print(f"Completed {product_id}", end=" , ")


if __name__ == '__main__':
    start = time.perf_counter()
    print("MultiThreading Started")
    get_multi_threaded(number_of_requests=25, max_threads=5)
    end = time.perf_counter()
    print("MultiThreading completed")
    print(f"Time taken: {end - start:.4f} seconds")

    start = time.perf_counter()
    print("Event Loop Started")
    asyncio.run(get_multi_task(number_of_requests=250))
    end = time.perf_counter()
    print("Event Loop completed")
    print(f"Time taken: {end - start:.4f} seconds")
