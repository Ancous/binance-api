import asyncio
import socket
import websockets.exceptions
import websockets
import json

from random import randint


async def get_stream_order_book_difference_spot(list_data: list,
                                                symbol_speed: list[list[str, str], ...],
                                                method: str = "SUBSCRIBE",
                                                my_id: int = randint(1, 100)) -> None:

    """
    Запрос:
    ...

    Полный url:
    "wss://stream.binance.com:9443/ws{symbol}@depth@{speed}ms"

    Параметры:
    - list_data (list): аргумент через который будут передаваться данные стрима ([])
    - symbol_speed (list[list[str, str], ...]): список данных по стриму - актив_скорость стрима ([["btcusdt", "100"], ["bnbusdt", "1000"], ...])
    - method (str): метод стрима ("SUBSCRIBE", "UNSUBSCRIBE")
    - my_id (int): идентификатор стрима (1, ..., 100)

    Комментарии:
    - скорость обновления: 100мс или 1000мс
    - symbol_speed вариант заполнения: [["btcusdt" или "bnbusdt" ...,  "100" или "1000"], ...]
    - symbol_speed значения должны быть строчными
    - method расшифровка ["SUBSCRIBE": подключить стрим, "UNSUBSCRIBE": отключить стрим, "LIST_SUBSCRIPTIONS": информация о стриме, "SET_PROPERTY": ..., "GET_PROPERTY": ...]

    Ответ:
    {
        "e": "depthUpdate",   (тип события)
        "E": 1571889248277,   (время события)
        "s": "BTCUSDT",   (символ)
        "U": 390497796,   (Идентификатор первого обновления в событии)
        "u": 390497878,   (Окончательный идентификатор обновления в событии)
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
    base_url = "wss://stream.binance.com:9443/ws"
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

                while True:
                    result = json.loads(await websocket.recv())
                    list_data[0] = result
                    print(result)
        except IndexError:
            list_data.append(None)
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

    data_streams = [["btcusdt", "1000"], ["adausdt", "1000"], ["bnbusdt", "1000"]]
    asyncio.run(get_stream_order_book_difference_spot(list_data=[], symbol_speed=data_streams))
