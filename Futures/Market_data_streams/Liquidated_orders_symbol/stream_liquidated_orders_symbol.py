import asyncio
import socket
import websockets.exceptions
import websockets
import json

from random import randint


async def get_stream_liquidated_orders_symbol(list_data: list,
                                              symbol: list[list[str], ...],
                                              method: str = "SUBSCRIBE",
                                              my_id: int = randint(1, 100)) -> None:

    """
    Запрос:
    Стрим ликвидированных ордеров по символу

    Полный url:
    "wss://fstream.binance.com/ws{symbol}@forceOrder"

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
        "e":"forceOrder",   (тип события)
        "E":1568014460893,   (время события)
        "o":{
            "s":"BTCUSDT",   (символ)
            "S":"SELL",   (сторона)
            "o":"LIMIT",   (тип ордера)
            "f":"IOC",   (Time in Force)
            "q":"0.014",   (количество)
            "p":"9910",   (цена)
            "ap":"9910",   (средняя цена)
            "X":"FILLED",   (статус ордера)
            "l":"0.014",   (Order Last Filled Quantity)
            "z":"0.014",   (Order Filled Accumulated Quantity)
            "T":1568014460893,   (время исполнения ордера)
        }
    }
    """

    # ----------------------------------------------
    base_url = "wss://fstream.binance.com/ws"
    streams = [f"{data[0].lower()}@forceOrder" for data in symbol]
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
                        print("Стрим ликвидированных ордеров по символу запущен.")
        except websockets.exceptions.ConnectionClosedError:
            print("Стрим ликвидированных ордеров по символу разрыв соединения. Восстанавливаем.\n"
                  "Ошибка: websockets.exceptions.ConnectionClosedError.")
            await asyncio.sleep(10)
        except socket.gaierror:
            print("Стрим ликвидированных ордеров по символу разрыв соединения. Восстанавливаем.\n"
                  "Ошибка: socket.gaierror.")
            await asyncio.sleep(10)


if __name__ in "__main__":

    data_streams = [["btcusdt"], ["adausdt"], ["bnbusdt"]]
    asyncio.run(get_stream_liquidated_orders_symbol(list_data=[], symbol=data_streams))
