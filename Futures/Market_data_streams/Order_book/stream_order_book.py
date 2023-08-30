import asyncio
import socket
import websockets.exceptions
import websockets
import json

from random import randint


async def get_stream_order_book(list_data: list,
                                symbol_quantity_speed: list[list[str, str, str], ...],
                                method: str = "SUBSCRIBE",
                                my_id: int = randint(1, 100)) -> None:
  
    """
    Запрос:
    Стрим стакана ордеров

    Полный url:
    "wss://fstream.binance.com/ws{symbol}@depth{quantity}@{speed}ms"

    Параметры:
    - list_data (list): аргумент через который будут передаваться данные стрима ([])
    - symbol_quantity_speed (list[list[str, str, str], ...]): список данных по стриму - актив_глубина стакана_скорость стрима ([["btcusdt", "10", "100"], ["bnbusdt", "5", "250"], ...])
    - method (str): метод стрима ("SUBSCRIBE", "UNSUBSCRIBE")
    - my_id (int): идентификатор стрима (1, ..., 100)

    Комментарии:
    - symbol_quantity_speed вариант заполнения: [["btcusdt" или "bnbusdt" и т.д., "5" или "10" или "20",  "100" или "250" или "500"], ...]
    - symbol_quantity_speed значения должны быть строчными
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
        "b": [   (bids)
                [
                    "7403.89",   (цена)
                    "0.002"   (количество)
                ],
                [
                    "7403.90",
                    "3.906"
                ],
                [
                    "7404.00",
                    "1.428"
                ],
                [
                    "7404.85",
                    "5.239"
                ],
                [
                    "7405.43",
                    "2.562"
                ]
            ],
        "a": [   (asks)
                [
                    "7405.96",   (цена)
                    "3.340"   (количество)
                ],
                [
                    "7406.63",
                    "4.525"
                ],
                [
                    "7407.08",
                    "2.475"
                ],
                [
                    "7407.15",
                    "4.800"
                ],
                [
                    "7407.20",
                    "0.175"
                ]
            ]
    }
    """

    # ----------------------------------------------
    base_url = "wss://fstream.binance.com/ws"
    streams = [f"{data[0].lower()}@depth{data[1]}@{data[2]}ms" for data in symbol_quantity_speed]
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
                        print("Стрим стакана ордеров запушен")
        except websockets.exceptions.ConnectionClosedError:
            print("Стрим стакана ордеров разрыв соединения. Восстанавливаем.\n"
                  "Ошибка: websockets.exceptions.ConnectionClosedError.")
            await asyncio.sleep(10)
        except socket.gaierror:
            print("Стрим стакана ордеров разрыв соединения. Восстанавливаем.\n"
                  "Ошибка: socket.gaierror.")
            await asyncio.sleep(10)


if __name__ in "__main__":

    data_streams = [["adausdt", "5", "500"]]
    asyncio.run(get_stream_order_book(list_data=[], symbol_quantity_speed=data_streams))
