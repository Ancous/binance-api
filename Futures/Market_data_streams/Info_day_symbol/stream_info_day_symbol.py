import asyncio
import socket
import websockets.exceptions
import websockets
import json

from random import randint


async def get_stream_info_day_symbol(list_data: list,
                                     symbol: list[list[str], ...],
                                     method: str = "SUBSCRIBE",
                                     my_id: int = randint(1, 100)) -> None:

    """
    Запрос:
    Стрим по информации об определенном символе за 24 часа

    Полный url:
    "wss://fstream.binance.com/ws{symbol}@ticker"

    Параметры:
    - list_data (list): аргумент через который будут передаваться данные стрима ([])
    - symbol (list[list[str], ...]): список символов ([["btcusdt"], ["bnbusdt"], ...])
    - method (str): метод стрима ("SUBSCRIBE", "UNSUBSCRIBE")
    - my_id (int): идентификатор стрима (1, ..., 100)

    Комментарии:
    - Это НЕ статистика дня UTC, а 24-часовое скользящее окно от времени запроса.
    - symbol вариант заполнения: [["btcusdt"], ...]
    - symbol значения должны быть строчными
    - method расшифровка ["SUBSCRIBE": подключить стрим, "UNSUBSCRIBE": отключить стрим, "LIST_SUBSCRIPTIONS": информация о стриме, "SET_PROPERTY": ..., "GET_PROPERTY": ...]

    Ответ:
    {
        "e": "24hrTicker",   (тип события)
        "E": 123456789,   (время события)
        "s": "BTCUSDT",   (символ)
        "p": "0.0015",   (изменение цены)
        "P": "250.00",   (изменение цены в процентах)
        "w": "0.0018",   (Weighted average price)
        "c": "0.0025",  (последняя цена)
        "Q": "10",   (последнее количество)
        "o": "0.0010",   (цена открытия)
        "h": "0.0025",   (максимальная цена)
        "l": "0.0010",   (минимальная цена)
        "v": "10000",   (общий торгуемый объем базовых активов)
        "q": "18",   (Общий торгуемый объем котировочного актива)
        "O": 0,   (время открытия статистики)
        "C": 86400000,   (время закрытия статистики)
        "F": 0,   (идентификатор первой сделки)
        "L": 18150,   (идентификатор последней сделки)
        "n": 18151   (количество сделок)
    }
    """

    # ----------------------------------------------
    base_url = "wss://fstream.binance.com/ws"
    streams = [f"{data[0].lower()}@ticker" for data in symbol]
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
                        print("Стрим по информации об определенном символе за 24 часа запущен.")
        except websockets.exceptions.ConnectionClosedError:
            print("Стрим по информации об определенном символе за 24 часа разрыв соединения. Восстанавливаем.\n"
                  "Ошибка: websockets.exceptions.ConnectionClosedError.")
            await asyncio.sleep(10)
        except socket.gaierror:
            print("Стрим по информации об определенном символе за 24 часа разрыв соединения. Восстанавливаем.\n"
                  "Ошибка: socket.gaierror.")
            await asyncio.sleep(10)


if __name__ in "__main__":

    data_streams = [["btcusdt"], ["adausdt"], ["bnbusdt"]]
    asyncio.run(get_stream_info_day_symbol(list_data=[], symbol=data_streams))
