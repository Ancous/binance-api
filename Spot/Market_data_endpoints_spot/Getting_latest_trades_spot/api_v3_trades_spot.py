import requests
import json


def get_latest_trades_spot(symbol: str,
                           limit: str = "500") -> dict:

    """
    Запрос:
    Получить последние рыночные сделки спота

    Полный url:
    "https://api.binance.com/api/v3/trades"

    Вес запроса:
    1

    Параметры:
    - symbol="symbol" (str): актив ("BTCUSDT", ...)
    - limit="limit" (str): какое количество последних сделок вывести ("1", ..., "1000")

    Комментарии:
    - Рыночные сделки означают сделки, заполненные в книге заявок.
    - Будут возвращены только рыночные сделки, это означает, что сделки страхового фонда и сделки ADL не будут возвращены.

    Ответ:
    [
       {
          "id": 439850393,
          "price": "0.27210000",
          "qty": "18.80000000",
          "quoteQty": "5.11548000",
          "time": 1686674419294,
          "isBuyerMaker": false,
          "isBestMatch": true
       },
       {
          "id": 439850394,
          "price": "0.27200000",
          "qty": "56.80000000",
          "quoteQty": "15.44960000",
          "time": 1686674419693,
          "isBuyerMaker": true,
          "isBestMatch": true
       }
    ]
    """

    # ------------------------------------------
    base_url = "https://api.binance.com"
    end_point = "/api/v3/trades"
    parameters = {
        "symbol": symbol.upper(),
        "limit": limit
    }
    # ------------------------------------------

    complete_request = base_url + end_point
    complete_parameters = parameters

    response = requests.get(url=complete_request, params=complete_parameters)
    result = json.loads(response.text)

    if response.status_code == 200:
        with open("answer.json", "w") as file:
            json.dump(obj=result, fp=file, indent=3)
        return {"status_code": response.status_code, "result": result}
    else:
        return {"status_code": response.status_code, "code_error": result['code'], "text_error": result['msg']}


if __name__ in "__main__":

    get_latest_trades_spot(symbol="ADAUSDT")
