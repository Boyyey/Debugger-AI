import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, List, Any

_executor = ThreadPoolExecutor(max_workers=8)

def run_in_executor(func: Callable, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return loop.run_in_executor(_executor, lambda: func(*args, **kwargs))

async def gather_async(funcs: List[Callable[[], Any]]) -> List[Any]:
    tasks = [run_in_executor(f) for f in funcs]
    return await asyncio.gather(*tasks) 