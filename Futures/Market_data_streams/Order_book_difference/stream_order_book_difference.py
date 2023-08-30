import asyncio
import socket
import websockets.exceptions
import websockets
import json

from random import randint


async def get_stream_order_book_difference(list_data: list,
                                           symbol_speed: list[list[str, str], ...],
                                           method: str = "SUBSCRIBE",
                                           my_id: int = randint(1, 100)) -> None:

    """
    Запрос:
    ...

    Полный url:
    "wss://fstream.binance.com/ws{symbol}@depth@{speed}ms"

    Параметры:
    - list_data (list): аргумент через который будут передаваться данные стрима ([])
    - symbol_speed (list[list[str, str], ...]): список данных по стриму - актив_скорость стрима ([["btcusdt", "100"], ["bnbusdt", "250"], ...])
    - method (str): метод стрима ("SUBSCRIBE", "UNSUBSCRIBE")
    - my_id (int): идентификатор стрима (1, ..., 100)

    Комментарии:
    - symbol_speed вариант заполнения: [["btcusdt" или "bnbusdt" ...,  "100" или "250" или "500"], ...]
    - symbol_speed значения должны быть строчными
    - method расшифровка ["SUBSCRIBE": подключить стрим, "UNSUBSCRIBE": отключить стрим, "LIST_SUBSCRIPTIONS": информация о стриме, "SET_PROPERTY": ..., "GET_PROPERTY": ...]

    Ответ:
    {
        "e": "depthUpdate",   (тип события)
        "E": 1571889248277,   (время события)
        "T": 1571889248276,   (время запроса)
        "s": "BTCUSDT",   (символ)
        "U": 390497796,   (Идентификатор первого обновления в событии)
        "u": 390497878,   (Окончательный идентификатор обновления в событии)
        "pu": 390497794,   (Final update Id in last stream(ie `u` in last stream))
        "b": [   (Bids)
                [
                    "7403.89",  (цена)
                    "0.002"   (количество)
                ]
        ],
        "a": [   (Asks)
                [
                    "7405.96",   (цена)
                    "3.340"   (количество)
                ]
        ]
    }
    """

    # ----------------------------------------------
    base_url = "wss://fstream.binance.com/ws"
    streams = [f"{data[0].lower()}@depth@{data[1]}ms" for data in symbol_speed]
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
                await websocket.send(json.dumps(subscribe_request))

                while True:
                    result = json.loads(await websocket.recv())
                    if not "id" in result:
                        list_data.clear()
                        list_data.append(result)
                        print(list_data)
                    else:
                        print("... запущен.")
        except websockets.exceptions.ConnectionClosedError:
            print("... разрыв соединения. Восстанавливаем.\n"
                  "Ошибка: websockets.exceptions.ConnectionClosedError.")
            await asyncio.sleep(10)
        except socket.gaierror:
            print("... разрыв соединения. Восстанавливаем.\n"
                  "Ошибка: socket.gaierror.")
            await asyncio.sleep(10)


if __name__ in "__main__":

    data_streams = [["btcusdt", "500"], ["adausdt", "500"], ["bnbusdt", "500"]]
    asyncio.run(get_stream_order_book_difference(list_data=[], symbol_speed=data_streams))
