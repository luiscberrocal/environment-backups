import asyncio
import sys

from rich.progress import track


async def sleeper(val):
    await asyncio.sleep(5)
    print(f'Processing {val}')
    return val


async def scheduler():
    tasks = [sleeper(i) for i in range(100)]
    total_tasks = len(tasks)
    for task in track(
            asyncio.as_completed(tasks),
            description="Processing...",
            total=total_tasks,
    ):
        await task


def get_event_loop():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    if sys.platform.startswith("win"):
        if isinstance(loop, asyncio.SelectorEventLoop):
            loop = asyncio.ProactorEventLoop()
            asyncio.set_event_loop(loop)
    return loop


def run_coroutine(coro):
    loop = get_event_loop()
    aws = asyncio.ensure_future(coro)
    result = loop.run_until_complete(aws)
    return result


if __name__ == "__main__":
    run_coroutine(scheduler())
