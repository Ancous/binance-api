import requests
import json


def get_latest_trades(symbol: str,
                      limit: str = "500") -> dict:

    """
    Запрос:
    Получить последние рыночные сделки

    Полный url:
    "https://fapi.binance.com/fapi/v1/trades"

    Вес запроса:
    5

    Параметры:
    - symbol="symbol" (str): актив ("BTCUSDT", ...)
    - limit="limit" (str): какое количество последних сделок вывести ("1", ..., "1000")

    Комментарии:
    - Рыночные сделки означают сделки, заполненные в книге заявок.
    - Будут возвращены только рыночные сделки, это означает, что сделки страхового фонда и сделки ADL не будут возвращены.

    Ответ:
    [
       {
          "id": 3576719543,
          "price": "29377.90",
          "qty": "0.001",
          "quoteQty": "29.37",
          "time": 1681742436170,
          "isBuyerMaker": false
       },
       {
          "id": 3576719544,
          "price": "29377.90",
          "qty": "0.064",
          "quoteQty": "1880.18",
          "time": 1681742436170,
          "isBuyerMaker": false
       }
    ]
    """

    # ------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/trades"
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
        return {"status_code": response.status_code, "headers": response.headers, "result": result}
    else:
        return {"status_code": response.status_code, "headers": response.headers, "code_error": result['code'], "text_error": result['msg']}


if __name__ in "__main__":

    result_2 = get_latest_trades(symbol="ADAUSDT")

    if result_2["status_code"] == 200:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("result:", result_2["result"])
    else:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("code_error:", result_2["code_error"])
        print("text_error:", result_2["text_error"])
