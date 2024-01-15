import requests
import json

from urllib.parse import urlencode

def get_day_statistics_spot(list_symbols: list = None,
                              my_type: str = "FULL") -> dict:

    """
    Запрос:
    Получить статистику изменения цены спота за 24 часа

    Полный url:
    "https://api.binance.com/api/v3/ticker/24hr"

    Вес запроса:
    [[list_symbols, вес], [1-20, 2], [21-100: 40], [>101: 80]

    Параметры:
    - list_symbols="symbols" (list): актив (["BTCUSDT"], ["BTCUSDT", "ADAUSDT"], ...)
    - my_type="my_type" (str): ... ("FULL","MINI")

    Комментарии:
    - Будьте осторожны при доступе к этому без символа.

    Ответ:
    {
       "symbol": "ADAUSDT",
       "priceChange": "0.00480",
       "priceChangePercent": "1.231",
       "weightedAvgPrice": "0.38924",
       "lastPrice": "0.39460",
       "lastQty": "319",
       "openPrice": "0.38980",
       "highPrice": "0.39690",
       "lowPrice": "0.38100",
       "volume": "508284698",
       "quoteVolume": "197842455.04000",
       "openTime": 1683219000000,
       "closeTime": 1683305434349,
       "firstId": 915943818,   (Первый идентификатор сделки)
       "lastId": 916332946,   (Последний идентификатор сделки)
       "count": 389059   (Количество сделок)
    }
    """

    # ------------------------------------------
    base_url = "https://api.binance.com"
    end_point = "/api/v3/ticker/24hr"
    if list_symbols:
        parameters = {
            "symbols": [symbol.upper() for symbol in list_symbols],
            "type": my_type
        }
    else:
        parameters = {
            "type": my_type
        }
    # ---------------------------------------------

    complete_request = base_url + end_point
    complete_parameters = urlencode(parameters).replace('%2C+', ',').replace('%27', '%22')

    response = requests.get(url=complete_request, params=complete_parameters)
    result = json.loads(response.text)

    if response.status_code == 200:
        with open("answer.json", "w") as file:
            json.dump(obj=result, fp=file, indent=3)
        return {"status_code": response.status_code, "result": result}
    else:
        return {"status_code": response.status_code, "code_error": result['code'], "text_error": result['msg']}


if __name__ in "__main__":

    get_day_statistics_spot(list_symbols=["ADAUSDT"])
