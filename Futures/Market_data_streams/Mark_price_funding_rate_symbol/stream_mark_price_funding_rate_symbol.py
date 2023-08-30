import asyncio
import socket
import websockets.exceptions
import websockets
import json

from random import randint


async def get_stream_mark_price_funding_rate_symbol(list_data: list,
                                                    symbol: list[list[str], ...],
                                                    speed: str = "",
                                                    method: str = "SUBSCRIBE",
                                                    my_id: int = randint(1, 100)) -> None:

    """
    Запрос:
    Стрим цены маркировки (mark price) и ставки финансирования по символу

    Полный url:
    "wss://fstream.binance.com/ws{symbol}@markPrice{speed}"

    Параметры:
    - list_data (list): аргумент через который будут передаваться данные стрима ([])
    - symbol (list[list[str], ...]): список символов ([["btcusdt"], ["bnbusdt"], ...])
    - speed (str): скорость стрима ("", "@1s"),
    - method (str): метод стрима ("SUBSCRIBE", "UNSUBSCRIBE")
    - my_id (int): идентификатор стрима (1, ..., 100)

    Комментарии:
    - symbol вариант заполнения: [["btcusdt"], ...]
    - symbol значения должны быть строчными
    - speed возможные варианты ["" - 3сек., "@1s" - 1сек.]
    - method расшифровка ["SUBSCRIBE": подключить стрим, "UNSUBSCRIBE": отключить стрим, "LIST_SUBSCRIPTIONS": информация о стриме, "SET_PROPERTY": ..., "GET_PROPERTY": ...]

    Ответ:
    {
        "e": "markPriceUpdate",   (тип события)
        "E": 1562305380000,   (время события)
        "s": "BTCUSDT",   (символ)
        "p": "11794.15000000",   (цена маркировки)
        "i": "11784.62659091",   (цена индекса)
        "P": "11784.25641265",   (предполагаемая цена, полезна только в последний час перед началом расчета)
        "r": "0.00038167",   (ставка финансирования)
        "T": 1562306400000   (время следующего финансирования)
    }
    """

    # ----------------------------------------------
    base_url = "wss://fstream.binance.com/ws"
    streams = [f"{data[0].lower()}@markPrice{speed}" for data in symbol]
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
                        print("Стрим цены маркировки (mark price) и ставки финансирования по символу запущен.")
        except websockets.exceptions.ConnectionClosedError:
            print("Стрим цены маркировки (mark price) и ставки финансирования по символу разрыв соединения. Восстанавливаем.\n"
                  "Ошибка: websockets.exceptions.ConnectionClosedError.")
            await asyncio.sleep(10)
        except socket.gaierror:
            print("Стрим цены маркировки (mark price) и ставки финансирования по символу разрыв соединения. Восстанавливаем.\n"
                  "Ошибка: socket.gaierror.")
            await asyncio.sleep(10)


if __name__ in "__main__":

    data_streams = [["btcusdt"], ["adausdt"], ["bnbusdt"]]
    asyncio.run(get_stream_mark_price_funding_rate_symbol(list_data=[], symbol=data_streams))
