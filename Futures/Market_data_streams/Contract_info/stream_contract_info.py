import asyncio
import socket
import websockets.exceptions
import websockets
import json

from random import randint


async def get_stream_contract_info(list_data: list,
                                   method: str = "SUBSCRIBE",
                                   my_id: int = randint(1, 100)) -> None:

    """
    Запрос:
    ...

    Полный url:
    "wss://fstream.binance.com/ws!contractInfo"

    Параметры:
    - list_data (list): аргумент через который будут передаваться данные стрима ([])
    - method (str): метод стрима ("SUBSCRIBE", "UNSUBSCRIBE")
    - my_id (int): идентификатор стрима (1, ..., 100)

    Комментарии:
    - method расшифровка ["SUBSCRIBE": подключить стрим, "UNSUBSCRIBE": отключить стрим, "LIST_SUBSCRIPTIONS": информация о стриме, "SET_PROPERTY": ..., "GET_PROPERTY": ...]

    Ответ:
    {
        "e":"contractInfo",   (тип события)
        "E":1669356423908,   (время события)
        "s":"IOTAUSDT",   (символ)
        "ps":"IOTAUSDT",   (пара)
        "ct":"PERPETUAL",   (тип контракта)
        "dt":4133404800000,   (дата и время доставки)
        "ot":1569398400000,   (onboard date time)
        "cs":"TRADING",   (статус контракта)
        "bks":[
            {
                "bs":1,   (Notional bracket)
                "bnf":0,   (Floor notional of this bracket)
                "bnc":5000,   (Cap notional of this bracket)
                "mmr":0.01,   (Maintenance ratio for this bracket)
                "cf":0,   (Auxiliary number for quick calculation)
                "mi":21,   (минимальное кредитное плечо для этой группы)
                "ma":50   (максимальное кредитное плечо для этой группы)
            },
            {
                "bs":2,
                "bnf":5000,
                "bnc":25000,
                "mmr":0.025,
                "cf":75,
                "mi":11,
                "ma":20
            }
        ]
    }
    """

    # ----------------------------------------------
    base_url = "wss://fstream.binance.com/ws"
    streams = ["!contractInfo"]
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

    asyncio.run(get_stream_contract_info(list_data=[]))
