import asyncio
import socket
import websockets.exceptions
import websockets
import json

from random import randint


async def get_stream_candles_contract(list_data: list,
                                      symbol_contract_interval: list[list[str, str, str], ...],
                                      method: str = "SUBSCRIBE",
                                      my_id: int = randint(1, 100)) -> None:

    """
    Запрос:
    Стрим свечей по контракту

    Полный url:
    "wss://fstream.binance.com/ws{symbol}_{contract}@continuousKline_{interval}"

    Параметры:
    - list_data (list): аргумент через который будут передаваться данные стрима ([])
    - symbol_contract_interval (list[list[str, str, str], ...]): список данных по стриму - символ_контракт_интервал ([["btcusdt", "perpetual", "1m"], ["bnbusdt", "current_quarter", "5m"], ...])
    - method (str): метод стрима ("SUBSCRIBE", "UNSUBSCRIBE")
    - my_id (int): идентификатор стрима (1, ..., 100)

    Комментарии:
    - symbol_contract_interval вариант заполнения: [["btcusdt" или "bnbusdt" ..., "perpetual" или "current_quarter" или "next_quarter", "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", 8h, "12h", "1d", "3d", "1w", "1M"], ...]
    - symbol_contract_interval значения должны быть строчными
    - method расшифровка ["SUBSCRIBE": подключить стрим, "UNSUBSCRIBE": отключить стрим, "LIST_SUBSCRIPTIONS": информация о стриме, "SET_PROPERTY": ..., "GET_PROPERTY": ...]

    Ответ:
    {
        "e":"continuous_kline",   (тип события)
        "E":1607443058651,   (время события)
        "ps":"BTCUSDT",   (пара)
        "ct":"PERPETUAL"   (тип контракта)
        "k":{
                "t":1607443020000,   (время начала свечи)
                "T":1607443079999,   (время завершения свечи)
                "i":"1m",   (интервал)
                "f":116467658886,   (идентификатор первой сделки)
                "L":116468012423,   (идентификатор последний сделки)
                "o":"18787.00",   (цена открытия)
                "c":"18804.04",   (цена закрытия)
                "h":"18804.04",   (максимальная цена)
                "l":"18786.54",   (минимальная цена)
                "v":"197.664",   (объем)
                "n": 543,   (количество сделок)
                "x":false,   (закрыта ли свеча?)
                "q":"3715253.19494",   (объем котируемого актива)
                "V":"184.769",   (Taker buy volume)
                "Q":"3472925.84746",   (Taker buy quote asset volume)
                "B":"0"   (Ignore)
        }
    }
    """

    # ----------------------------------------------
    base_url = "wss://fstream.binance.com/ws"
    streams = [f"{data[0].lower()}_{data[1]}@continuousKline_{data[2]}" for data in symbol_contract_interval]
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
                        print("Стрим свечей по контракту запущен.")
        except websockets.exceptions.ConnectionClosedError:
            print("Стрим свечей по контракту разрыв соединения. Восстанавливаем.\n"
                  "Ошибка: websockets.exceptions.ConnectionClosedError.")
            await asyncio.sleep(10)
        except socket.gaierror:
            print("Стрим свечей по контракту разрыв соединения. Восстанавливаем.\n"
                  "Ошибка: socket.gaierror.")
            await asyncio.sleep(10)


if __name__ in "__main__":

    data_streams = [["btcusdt", "perpetual", "5m"], ["adausdt", "perpetual", "5m"], ["bnbusdt", "perpetual", "5m"]]
    asyncio.run(get_stream_candles_contract(list_data=[], symbol_contract_interval=data_streams))
