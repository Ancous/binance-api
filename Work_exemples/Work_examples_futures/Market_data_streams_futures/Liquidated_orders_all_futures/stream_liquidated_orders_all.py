"""
pass
"""

import asyncio
import os
from dotenv import load_dotenv

from binance_api_ancous import MarketDataStreamsFutures

load_dotenv()


async def my_print(list_data):
    """
    pass
    """
    while True:
        if not list_data:
            await asyncio.sleep(10)
        else:
            print(list_data)
            await asyncio.sleep(0.1)


async def func_main_stream(futures_client, list_data):
    """
    pass
    """
    task_1 = asyncio.create_task(futures_client.get_stream_liquidated_orders_all_futures(
        list_data=list_data)
    )
    task_2 = asyncio.create_task(my_print(
        list_data=list_data)
    )

    while True:
        try:
            await task_1
            await task_2
        except asyncio.CancelledError:
            task_1.cancel()
            task_2.cancel()
            print(f"Стрим не запустился")
            break


if __name__ in "__main__":
    my_list = list()
    client_mds = MarketDataStreamsFutures(secret_key=os.getenv("secret_key"), api_key=os.getenv("api_key"))

    asyncio.run(func_main_stream(
        futures_client=client_mds,
        list_data=my_list)
    )
