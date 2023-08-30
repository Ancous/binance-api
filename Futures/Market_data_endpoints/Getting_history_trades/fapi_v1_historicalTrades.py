import requests
import json
import os
from dotenv import load_dotenv


load_dotenv()


def get_historical_trades(symbol: str,
                          from_id: str = None,
                          limit: str = "500") -> dict:

    """
    Запрос:
    Получить исторические рыночные сделки по "fromId"

    Полный url:
    "https://fapi.binance.com/fapi/v1/historicalTrades"

    Вес запроса:
    20

    Параметры:
    - symbol="symbol" (str): актив ("BTCUSDT", ...)
    - from_id="fromId": (str): идентификатор сделки от которой будет произведён вывод следующих сделок ("567887", ...)
    - limit="limit" (str): какое исторических количество сделок вывести ("1", ..., "1000")

    Комментарии:
    - Рыночные сделки означают сделки, заполненные в книге заявок.
    - Если "fromId" не указан показывает самые последние сделки
    - Будут возвращены только рыночные сделки, это означает, что сделки страхового фонда и сделки ADL не будут возвращены.

    Ответ:
    [
       {
          "id": 3576730350,
          "price": "29341.00",
          "qty": "0.181",
          "quoteQty": "5310.72",
          "time": 1681742589853,
          "isBuyerMaker": true
       },
       {
          "id": 3576730351,
          "price": "29341.00",
          "qty": "0.174",
          "quoteQty": "5105.33",
          "time": 1681742589870,
          "isBuyerMaker": true
       }
    ]
    """

    # ------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/historicalTrades"
    api_key = os.getenv("api_key")
    parameters = {
        "symbol": symbol.upper(),
        "limit": limit,
        "fromId": from_id,
    }
    # ------------------------------------

    complete_request = base_url + end_point
    complete_parameters = parameters
    headers = {
        "X-MBX-APIKEY": api_key
    }

    response = requests.get(url=complete_request, params=complete_parameters, headers=headers)
    result = json.loads(response.text)

    if response.status_code == 200:
        with open("answer.json", "w") as file:
            json.dump(obj=result, fp=file, indent=3)
        return {"status_code": response.status_code, "headers": response.headers, "result": result}
    else:
        return {"status_code": response.status_code, "headers": response.headers, "code_error": result['code'], "text_error": result['msg']}


if __name__ in "__main__":

    result_2 = get_historical_trades(symbol="ADAUSDT")

    if result_2["status_code"] == 200:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("result:", result_2["result"])
    else:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("code_error:", result_2["code_error"])
        print("text_error:", result_2["text_error"])
