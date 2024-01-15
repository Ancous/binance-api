import asyncio
import socket
import time
import websockets.exceptions
import websockets
import json

from random import randint


async def get_stream_info_rolling_all_spot(list_data: list,
                                           winsizes: str,
                                           method: str = "SUBSCRIBE",
                                           my_id: int = randint(1, 100)) -> None:

    """
    Запрос:
    Стрим по информации о всех символах спота в скользящем окне

    Полный url:
    "wss://stream.binance.com:9443/ws!ticker_{window_size}@arr"

    Параметры:
    - list_data (list): аргумент через который будут передаваться данные стрима ([])
    - winsize (str): список размера окна ("1h", "4h", "1d")
    - method (str): метод стрима ("SUBSCRIBE", "UNSUBSCRIBE")
    - my_id (int): идентификатор стрима (1, ..., 100)

    Комментарии:
    - скорость обновления: 1000мс
    - Это НЕ статистика дня UTC, а 24-часовое скользящее окно от времени запроса.
    - winsizes значения должны быть строчными
    - method расшифровка ["SUBSCRIBE": подключить стрим, "UNSUBSCRIBE": отключить стрим, "LIST_SUBSCRIPTIONS": информация о стриме, "SET_PROPERTY": ..., "GET_PROPERTY": ...]

    Ответ:
    [
        {
            "e": "1hTicker",   (тип события)
            "E": 123456789,   (время события)
            "s": "BTCUSDT",   (символ)
            "p": "0.0015",   (изменение цены)
            "P": "250.00",   (изменение цены в процентах)
            "w": "0.0018",   (Weighted average price)
            "o": "0.0010",   (цена открытия)
            "h": "0.0025",   (максимальная цена)
            "l": "0.0010",   (минимальная цена)
            "c": "0.0025",  (последняя цена)
            "v": "10000",   (общий торгуемый объем базовых активов)
            "q": "18",   (Общий торгуемый объем котировочного актива)
            "O": 0,   (время открытия статистики)
            "C": 86400000,   (время закрытия статистики)
            "F": 0,   (идентификатор первой сделки)
            "L": 18150,   (идентификатор последней сделки)
            "n": 18151   (количество сделок)
        }
    ]
    """

    # ----------------------------------------------
    base_url = "wss://stream.binance.com:9443/ws"
    streams = [f"!ticker_{winsizes}@arr"]
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
            print("Стрим по информации о всех символах спота в скользящем окне запущен.")
        except websockets.exceptions.ConnectionClosedError:
            print("Стрим по информации о всех символах спота в скользящем окне разрыв соединения. Восстанавливаем.\n"
                  "Ошибка: websockets.exceptions.ConnectionClosedError.")
            await asyncio.sleep(10)
        except socket.gaierror:
            print("Стрим по информации о всех символах спота в скользящем окне разрыв соединения. Восстанавливаем.\n"
                  "Ошибка: socket.gaierror.")
            await asyncio.sleep(10)


if __name__ in "__main__":

    asyncio.run(get_stream_info_rolling_all_spot(list_data=[], winsizes="1h"))
