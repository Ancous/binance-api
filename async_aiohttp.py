import time
from typing import Any
import asyncio

from aiohttp import ClientSession


async def get_blvt_klines(symbol: str,
                          interval: str,
                          limit: int,
                          start_time: int = "",
                          end_time: int = "") -> Any:
    # ---------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/lvtKlines"
    parameters = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit,
        "startTime": start_time,
        "endTime": end_time
    }
    # ---------------------------------------------

    complete_request = base_url + end_point
    complete_parameters = parameters

    async with ClientSession() as session:
        async with session.get(url=complete_request, params=complete_parameters) as response:
            data = await response.json()

    if response.status == 200:
        print(data)
    else:
        result = f"ОШИБКА!!!\nСтатус-код ответа: {response.status}\nКод ошибки: {data['code']}\nТекст ошибки: {data['msg']}"
        print(result)


async def main():
    task_1 = asyncio.create_task(get_blvt_klines(symbol="BTCDOWN", interval="1m", limit=1))
    task_2 = asyncio.create_task(get_blvt_klines(symbol="BTCDOWN", interval="1m", limit=1))
    task_3 = asyncio.create_task(get_blvt_klines(symbol="BTCDOWN", interval="1m", limit=1))

    await task_1
    await task_2
    await task_3

if __name__ in "__main__":
    start = time.time()
    asyncio.run(main())
    print(f"Асинхронное время выполнения: {time.time() - start} секунд.")
