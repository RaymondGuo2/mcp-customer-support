import asyncio, httpx, time

async def bench_rest(n=1000):
    url = "http://127.0.0.1:8000/tickets/T123"
    async with httpx.AsyncClient() as client:
        start = time.perf_counter()
        for _ in range(n):
            r = await client.get(url)
            r.raise_for_status()
        elapsed = time.perf_counter() - start
        print(f"REST {n} calls in {elapsed:.2f}s → {n/elapsed:.1f} req/s")

asyncio.run(bench_rest())
