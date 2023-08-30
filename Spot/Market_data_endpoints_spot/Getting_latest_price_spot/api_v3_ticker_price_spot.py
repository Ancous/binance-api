import requests
import json

from urllib.parse import urlencode


def get_latest_price_spot(list_symbols: list = None) -> dict:

    """
    Запрос:
    Получить последнюю цену для символа или символов спота

    Полный url:
    "https://api.binance.com/api/v3/ticker/price"

    Вес запроса:
    1 для одного символа, 2 когда параметр символа отсутствует

    Параметры:
    - list_symbols="symbols" (list): актив (["BTCUSDT"], ["BTCUSDT", "ADAUSDT"], ...)

    Комментарии:
    - None

    Ответ:
    [
       {
          "symbol": "ADAUSDT",
          "price": "0.27360000"
       }
    ]
    """

    # ------------------------------------------
    base_url = "https://api.binance.com"
    end_point = "/api/v3/ticker/price"
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

    get_latest_price_spot(list_symbols=["ADAUSDT"])
