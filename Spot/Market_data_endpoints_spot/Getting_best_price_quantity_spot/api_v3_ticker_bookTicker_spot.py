import requests
import json

from urllib.parse import urlencode


def get_best_price_quantity_spot(list_symbols: list = None) -> dict:

    """
    Запрос:
    Получить лучшую цену и количество для символа или символов спота

    Полный url:
    "https://api.binance.com/api/v3/ticker/bookTicker"

    Вес запроса:
    2 для одного символа, 4 когда параметр символа отсутствует

    Параметры:
    - list_symbols="symbols" (list): актив (["BTCUSDT"], ["BTCUSDT", "ADAUSDT"], ...)

    Комментарии:
    - None

    Ответ:
    [
       {
          "symbol": "ADAUSDT",
          "bidPrice": "0.27340000",
          "bidQty": "6235.10000000",
          "askPrice": "0.27350000",
          "askQty": "40243.50000000"
       }
    ]
    """

    # ------------------------------------------
    base_url = "https://api.binance.com"
    end_point = "/api/v3/ticker/bookTicker"
    if list_symbols:
        parameters = {
                "symbols": [symbol.upper() for symbol in list_symbols]
            }
    else:
        parameters = {}
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

    get_best_price_quantity_spot(list_symbols=["ADAUSDT"])
