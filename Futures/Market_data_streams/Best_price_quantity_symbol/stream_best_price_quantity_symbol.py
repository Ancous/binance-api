import asyncio
import socket
import websockets.exceptions
import websockets
import json

from random import randint


async def get_stream_best_price_quantity_symbol(list_data: list,
                                                symbol: list[list[str], ...],
                                                method: str = "SUBSCRIBE",
                                                my_id: int = randint(1, 100)) -> None:

    """
    Запрос:
    Стрим лучшей цены и количества по символу


    Полный url:
    "wss://fstream.binance.com/ws{symbol}@bookTicker"

    Параметры:
    - list_data (list): аргумент через который будут передаваться данные стрима ([])
    - symbol (list[list[str], ...]): список символов ([["btcusdt"], ["bnbusdt"], ...])
    - method (str): метод стрима ("SUBSCRIBE", "UNSUBSCRIBE")
    - my_id (int): идентификатор стрима (1, ..., 100)

    Комментарии:
    - symbol вариант заполнения: [["btcusdt"], ...]
    - symbol значения должны быть строчными
    - method расшифровка ["SUBSCRIBE": подключить стрим, "UNSUBSCRIBE": отключить стрим, "LIST_SUBSCRIPTIONS": информация о стриме, "SET_PROPERTY": ..., "GET_PROPERTY": ...]

    Ответ:
    {
        "e":"bookTicker",   (тип события)
        "u":400900217,   (идентификатор обновления книги заказов)
        "s":"BNBUSDT",   (символ)
        "b":"25.35190000",   (лучшая цена bid)
        "B":"31.21000000",   (лучшая ставка bid)
        "a":"25.36520000",   (лучшая цена ask)
        "A":"40.66000000"   (лучшая ставка ask)
        "T": 1568014460891,   (время транзакции)
        "E": 1568014460893,   (время события)
    }
    """

    # ----------------------------------------------
    base_url = "wss://fstream.binance.com/ws"
    streams = [f"{data[0].lower()}@bookTicker" for data in symbol]
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
                        print("Стрим лучшей цены и количества по символу запущен.")
        except websockets.exceptions.ConnectionClosedError:
            print("Стрим лучшей цены и количества по символу разрыв соединения. Восстанавливаем.\n"
                  "Ошибка: websockets.exceptions.ConnectionClosedError.")
            await asyncio.sleep(10)
        except socket.gaierror:
            print("Стрим лучшей цены и количества по символу разрыв соединения. Восстанавливаем.\n"
                  "Ошибка: socket.gaierror.")
            await asyncio.sleep(10)


if __name__ in "__main__":

    data_streams = [["btcusdt"], ["adausdt"], ["bnbusdt"]]
    asyncio.run(get_stream_best_price_quantity_symbol(list_data=[], symbol=data_streams))
