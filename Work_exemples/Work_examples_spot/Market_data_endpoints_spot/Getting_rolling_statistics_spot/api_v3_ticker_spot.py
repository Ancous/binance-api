import requests
import json

from urllib.parse import urlencode

def get_rolling_statistics_spot(list_symbols: list,
                                window_size: str = "1d",
                                my_type: str = "FULL") -> dict:

    """
    Запрос:
    Получить статистику изменения цены спота в скользящем окне

    Полный url:
    "https://api.binance.com/api/v3/ticker"

    Вес запроса:
    4 для каждого запрошенного символа независимо от размера окна
    Макс 200, если количество символов в запросе превысит 50.

    Параметры:
    - list_symbols="symbols" (list): актив (["BTCUSDT"], ["BTCUSDT", "ADAUSDT"], ...)
    - window_size="windowSize" (str): ... ("1m", "7m", "23", ...."59m" - минута, "1h", "13h", ...."23h" - час, "1d", ..."7d" - день)

    - my_type="my_type" (str): ... ("FULL","MINI")

    Комментарии:
    - Будьте осторожны при доступе к этому без символа.

    Ответ:
    [
       {
          "symbol": "ADAUSDT",
          "priceChange": "-0.00140000",
          "priceChangePercent": "-0.508",
          "weightedAvgPrice": "0.27829560",
          "openPrice": "0.27540000",
          "highPrice": "0.28960000",
          "lowPrice": "0.26840000",
          "lastPrice": "0.27400000",
          "volume": "164931358.20000000",
          "quoteVolume": "45899670.84442000",
          "openTime": 1686597120000,
          "closeTime": 1686683573607,
          "firstId": 439721518,
          "lastId": 439858217,
          "count": 136700
       }
    ]
    """

    # ------------------------------------------
    base_url = "https://api.binance.com"
    end_point = "/api/v3/ticker"
    if list_symbols:
        parameters = {
            "symbols": [symbol.upper() for symbol in list_symbols],
            "windowSize": window_size,
            "type": my_type
        }
    else:
        parameters = {
            "windowSize": window_size,
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

    get_rolling_statistics_spot(list_symbols=["ADAUSDT"])
