import asyncio
import socket
import websockets.exceptions
import websockets
import json

from random import randint


async def get_stream_trades_tape(list_data: list,
                                 symbol: list[list[str], ...],
                                 method: str = "SUBSCRIBE",
                                 my_id: int = randint(1, 100)) -> None:

    """
    Запрос:
    Стрим ленты сделок по символу

    Полный url:
    "wss://fstream.binance.com/ws{symbol}@aggTrade"

    Параметры:
    - list_data (list): аргумент через который будут передаваться данные стрима ([])
    - symbol (list[list[str], ...]): список символов ([["btcusdt"], ["bnbusdt"], ...])
    - method (str): метод стрима ("SUBSCRIBE", "UNSUBSCRIBE")
    - my_id (int): идентификатор стрима (1, ..., 100)

    Комментарии:
    - symbol вариант заполнения: [["btcusdt"], ...]
    - symbol значения должны быть строчными
    - method расшифровка ["SUBSCRIBE": подключить стрим, "UNSUBSCRIBE": отключить стрим, "LIST_SUBSCRIPTIONS": информация о стриме, "SET_PROPERTY": ..., "GET_PROPERTY": ...]
    - Будут агрегированы только рыночные сделки, что означает, что сделки страхового фонда и сделки ADL не будут агрегированы.

    Ответ:
    {
        "e": "aggTrade",   (тип события)
        "E": 123456789,   (время события)
        "s": "BTCUSDT",   (символ)
        "a": 5933014,   (идентификатор сделки)
        "p": "0.001",   (цена)
        "q": "100",   (количество)
        "f": 100,   (идентификатор первой сделки)
        "l": 105,   (идентификатор последний сделки)
        "T": 123456785,   (время торговли)
        "m": true,   (является ли покупатель маркет-мейкером?)
    }
    """

    # ----------------------------------------------
    base_url = "wss://fstream.binance.com/ws"
    streams = [f"{data[0].lower()}@aggTrade" for data in symbol]
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
                        print("Стрим ленты сделок по символу запущен.")
        except websockets.exceptions.ConnectionClosedError:
            print("Стрим ленты сделок по символу разрыв соединения. Восстанавливаем.\n"
                  "Ошибка: websockets.exceptions.ConnectionClosedError.")
            await asyncio.sleep(10)
        except socket.gaierror:
            print("Стрим ленты сделок по символу разрыв соединения. Восстанавливаем.\n"
                  "Ошибка: socket.gaierror.")
            await asyncio.sleep(10)


if __name__ in "__main__":

    data_streams = [["btcusdt"], ["adausdt"], ["bnbusdt"]]
    asyncio.run(get_stream_trades_tape(list_data=[], symbol=data_streams))
