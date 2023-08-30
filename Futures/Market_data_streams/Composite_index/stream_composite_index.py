import asyncio
import socket
import websockets.exceptions
import websockets
import json

from random import randint


async def get_stream_composite_index(list_data: list,
                                     composite_index: list[list[str], ...],
                                     method: str = "SUBSCRIBE",
                                     my_id: int = randint(1, 100)) -> None:

    """
    Запрос:
    Стрим стакана ордеров составного индекса

    Полный url:
    "wss://fstream.binance.com/ws{composite_index}@compositeIndex"

    Параметры:
    - list_data (list): аргумент через который будут передаваться данные стрима ([])
    - composite_index (list[list[str], ...]): список составных индексов ([["defiusdt"], ...])
    - method (str): метод стрима ("SUBSCRIBE", "UNSUBSCRIBE")
    - my_id (int): идентификатор стрима (1, ..., 100)

    Комментарии:
    - composite_index значения должны быть строчными
    - method расшифровка ["SUBSCRIBE": подключить стрим, "UNSUBSCRIBE": отключить стрим, "LIST_SUBSCRIPTIONS": информация о стриме, "SET_PROPERTY": ..., "GET_PROPERTY": ...]

    Ответ:
    {
        "e":"compositeIndex",   (тип события)
        "E":1602310596000,   (время события)
        "s":"DEFIUSDT",   (символ)
        "p":"554.41604065",   (цена)
        "C":"baseAsset",
        "c":[   (состав)
            {
                "b":"BAL",   (базовый актив)
                "q":"USDT",   (актив котировки)
                "w":"1.04884844",   (вес в количестве)
                "W":"0.01457800",   (вес в процентах)
                "i":"24.33521021"   (цена индекса)
            },
            {
                "b":"BAND",
                "q":"USDT" ,
                "w":"3.53782729",
                "W":"0.03935200",
                "i":"7.26420084"
            }
        ]
    }
    """

    # ----------------------------------------------
    base_url = "wss://fstream.binance.com/ws"
    streams = [f"{data[0].lower()}@compositeIndex" for data in composite_index]
    # ----------------------------------------------

    while True:
        try:
            async with websockets.connect(base_url) as websocket:
                subscribe_request = {
                    "method": method,
                    "params": streams,
                    "id": my_id,
                }
                await websocket.send(json.dumps(subscribe_request))

                while True:
                    result = json.loads(await websocket.recv())
                    if not "id" in result:
                        list_data.clear()
                        list_data.append(result)
                        print(list_data)
                    else:
                        print("Стрим стакана ордеров составного индекса запущен.")
        except websockets.exceptions.ConnectionClosedError:
            print("Стрим стакана ордеров составного индекса разрыв соединения. Восстанавливаем.\n"
                  "Ошибка: websockets.exceptions.ConnectionClosedError.")
            await asyncio.sleep(10)
        except socket.gaierror:
            print("Стрим стакана ордеров составного индекса разрыв соединения. Восстанавливаем.\n"
                  "Ошибка: socket.gaierror.")
            await asyncio.sleep(10)


if __name__ in "__main__":

    data_streams = [["defiusdt"]]
    asyncio.run(get_stream_composite_index(list_data=[], composite_index=data_streams))
