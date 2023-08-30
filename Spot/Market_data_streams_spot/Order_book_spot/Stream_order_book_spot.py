import asyncio
import socket
import websockets.exceptions
import websockets
import json

from random import randint


async def get_stream_order_book_spot(list_data: list,
                                     symbol_quantity_speed: list[list[str, str, str]],
                                     method: str = "SUBSCRIBE",
                                     my_id: int = randint(1, 100)) -> None:
    """
    Запрос:
    Стрим стакана ордеров спота

    Полный url:
    "wss://stream.binance.com:9443/ws{symbol}@depth{quantity}@{speed}ms"

    Параметры:
    - list_data (list): аргумент в который будут записываться данные стрима ([])
    - symbol_quantity_speed (list[list[str, str, str]]): список данных по стрима - актив_глубина стакана_скорость стрима ([["btcusdt", "10", "100"]])
    - method (str): метод стрима ("SUBSCRIBE", "UNSUBSCRIBE")
    - my_id (int): идентификатор стрима (1, ..., 100)

    Комментарии:
    - скорость обновления: 100мс или 1000мс
    - symbol_quantity_speed вариант заполнения: [["btcusdt" или "bnbusdt" и т.д., "5" или "10" или "20",  "100" или "1000"]
    - symbol_quantity_speed значения должны быть строчными
    - method расшифровка ["SUBSCRIBE": подключить стрим, "UNSUBSCRIBE": отключить стрим, "LIST_SUBSCRIPTIONS": информация о стриме, "SET_PROPERTY": ..., "GET_PROPERTY": ...]

    Ответ:
    {
        'lastUpdateId': 7379433651,   (идентификатор последнего обновления)
        'bids':[   (Bids)
            [
                '0.26080000',   (обновляемый уровень цены)
                '35190.90000000'   (количество)
            ],
        ],
        'asks':[   (Asks)
            [
                '0.26090000',   (обновляемый уровень цены)
                '36457.60000000'   (количество)
            ],
        ]
    }
    """

    # ----------------------------------------------
    base_url = "wss://stream.binance.com:9443/ws"
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
                    list_data[0] = result
                    print(result)
        except IndexError:
            list_data.append(None)
            print("Стрим стакана ордеров спота запущен.")
        except websockets.exceptions.ConnectionClosedError:
            print("Стрим стакана ордеров спота разрыв соединения. Восстанавливаем.\n"
                  "Ошибка: websockets.exceptions.ConnectionClosedError.")
            await asyncio.sleep(10)
        except socket.gaierror:
            print("Стрим стакана ордеров спота разрыв соединения. Восстанавливаем.\n"
                  "Ошибка: socket.gaierror.")
            await asyncio.sleep(10)


if __name__ in "__main__":

    data_streams = [["btcusdt", "5", "1000"]]
    asyncio.run(get_stream_order_book_spot(list_data=[], symbol_quantity_speed=data_streams))
