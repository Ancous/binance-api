import asyncio
import socket
import websockets.exceptions
import websockets
import json

from random import randint


async def get_stream_min_info_day_all_spot(list_data: list,
                                           method: str = "SUBSCRIBE",
                                           my_id: int = randint(1, 100)) -> None:

    """
    Запрос:
    Стрим по минимальной информации о всех символах спота за 24 часа

    Полный url:
    "wss://stream.binance.com:9443/ws!miniTicker@arr"

    Параметры:
    - list_data (list): аргумент через который будут передаваться данные стрима ([])
    - method (str): метод стрима ("SUBSCRIBE", "UNSUBSCRIBE")
    - my_id (int): идентификатор стрима (1, ..., 100)

    Комментарии:
    - скорость обновления: 1000мс
    - Это НЕ статистика дня UTC, а 24-часовое скользящее окно от времени запроса.
    - Обратите внимание, что в массиве будут присутствовать только измененные тикеры.
    - method расшифровка ["SUBSCRIBE": подключить стрим, "UNSUBSCRIBE": отключить стрим, "LIST_SUBSCRIPTIONS": информация о стриме, "SET_PROPERTY": ..., "GET_PROPERTY": ...]

    Ответ:
    [
        {
            "e": "24hrMiniTicker",   (тип события)
            "E": 123456789,   (время события)
            "s": "BTCUSDT",   (символ)
            "c": "0.0025",   (цена закрытия)
            "o": "0.0010",   (цена открытия)
            "h": "0.0025",   (максимальная цена)
            "l": "0.0010",   (минимальная цена)
            "v": "10000",   (Total traded base asset volume)
            "q": "18"   (Total traded quote asset volume)
        }
    ]
    """

    # ----------------------------------------------
    base_url = "wss://stream.binance.com:9443/ws"
    streams = ["!miniTicker@arr"]
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
            print("Стрим по минимальной информации о всех символах спота за 24 часа запущен.")
        except websockets.exceptions.ConnectionClosedError:
            print("Стрим по минимальной информации о всех символах спота за 24 часа разрыв соединения. Восстанавливаем.\n"
                  "Ошибка: websockets.exceptions.ConnectionClosedError.")
            await asyncio.sleep(10)
        except socket.gaierror:
            print("Стрим по минимальной информации о всех символах спота за 24 часа разрыв соединения. Восстанавливаем.\n"
                  "Ошибка: socket.gaierror.")
            await asyncio.sleep(10)


if __name__ in "__main__":

    asyncio.run(get_stream_min_info_day_all_spot(list_data=[]))
