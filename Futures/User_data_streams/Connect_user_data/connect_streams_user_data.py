import asyncio
import socket
import time
import websockets.exceptions
import websockets
import json

from random import randint

from Futures.User_data_streams.Start_user_data.start_streams_user_data import start_user_data_stream


async def connect_user_data_streams(dict_data: dict,
                                    listen_key: str,
                                    method: str = "SUBSCRIBE",
                                    my_id: int = randint(1, 100)) -> None:

    """
    Запрос:
    Стрим для получения данных пользователя

    Полный url:
   "wss://fstream.binance.com/ws{listenKey}"

    Параметры:
    - list_data (list): аргумент через который будут передаваться данные стрима ([])
    - listenKey (str): ... ("LHW0SdJy0FuOISIN5MBDGDV0V2s2WjPSaKdpCLh5yQ31EH97OiNwI6tnhlidndAoe")
    - method (str): метод стрима ("SUBSCRIBE", "UNSUBSCRIBE")
    - my_id (int): идентификатор стрима (1, ..., 100)

    Комментарии:
    - listenKey можно получить по запросу через url "https://fapi.binance.com/fapi/v1/listenKey"

    Ответ:
    {
       "listenKey": "xVAUfwyLHjbiReNjOC1Xy0OU88UPzFke7LEjc2AmYi8GPIApGSdu492wzKkXrhQW"
    }
    """

    # ----------------------------------------------
    base_url_stream = "wss://fstream.binance.com/ws"
    # ----------------------------------------------

    while True:
        try:
            async with websockets.connect(base_url_stream) as websocket:
                subscribe_request = {
                    "method": method,
                    "params": [listen_key],
                    "id": my_id,
                }
                await websocket.send(json.dumps(subscribe_request))

                while True:
                    result = json.loads(await websocket.recv())
                    if not "id" in result:
                        dict_data[result["e"].lower()] = result
                        print(dict_data)
                    else:
                        print("Стрим для получения данных пользователя запущен")
        except websockets.exceptions.ConnectionClosedError:
            print("Стрим для получения данных пользователя разрыв соединения. Восстанавливаем.\n"
                  "Ошибка: websockets.exceptions.ConnectionClosedError.")
            time.sleep(10)
        except socket.gaierror:
            print("Стрим для получения данных пользователя разрыв соединения. Восстанавливаем.\n"
                  "Ошибка: socket.gaierror.")
            time.sleep(10)


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

    response = start_user_data_stream()
    my_listen_key = response["result"]["listenKey"]
    asyncio.run(connect_user_data_streams(dict_data=event_data, listen_key=my_listen_key))
