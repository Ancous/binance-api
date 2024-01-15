"""
pass
"""

import asyncio
import os
from dotenv import load_dotenv

from Futures import UserDataStreamsFutures

load_dotenv()


async def my_print(dict_data):
    """
    pass
    """
    while True:
        if not dict_data:
            await asyncio.sleep(10)
        else:
            print(dict_data)
            await asyncio.sleep(0.1)


async def func_main_stream(futures_client, dict_data, listen_key):
    """
    pass
    """
    task_1 = asyncio.create_task(futures_client.connect_user_data_streams_futures(
        dict_data=dict_data,
        listen_key=listen_key)
    )
    task_2 = asyncio.create_task(my_print(
        dict_data=dict_data)
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
    event_data = dict(
        listenKeyExpired=None,
        margin_call=None,
        account_update=None,
        order_trade_update=None,
        account_config_update=None,
        strategy_update=None,
        grid_update=None,
        conditional_order_trigger_reject=None
    )

    client_uds = UserDataStreamsFutures(secret_key=os.getenv("secret_key"), api_key=os.getenv("api_key"))
    response = client_uds.start_user_data_stream_futures()
    my_listen_key = response["result"]["listenKey"]

    asyncio.run(func_main_stream(
        futures_client=client_uds,
        dict_data=event_data,
        listen_key=my_listen_key)
    )
