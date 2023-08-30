import requests
import json
import os

from dotenv import load_dotenv


load_dotenv()


def get_historical_trades_spot(symbol: str,
                               from_id: str = None,
                               limit: str = "500") -> dict:

    """
    Запрос:
    Получить исторические рыночные сделки по "fromId" спота

    Полный url:
    "https://api.binance.com/api/v3/historicalTrades"

    Вес запроса:
    5

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
          "id": 439851294,
          "price": "0.27280000",
          "qty": "631.10000000",
          "quoteQty": "172.16408000",
          "time": 1686675498135,
          "isBuyerMaker": false,
          "isBestMatch": true
       },
       {
          "id": 439851295,
          "price": "0.27270000",
          "qty": "144.10000000",
          "quoteQty": "39.29607000",
          "time": 1686675501547,
          "isBuyerMaker": true,
          "isBestMatch": true
       }
    ]
    """

    # ------------------------------------
    base_url = "https://api.binance.com"
    end_point = "/api/v3/historicalTrades"
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
        return {"status_code": response.status_code, "result": result}
    else:
        return {"status_code": response.status_code, "code_error": result['code'], "text_error": result['msg']}


if __name__ in "__main__":

    get_historical_trades_spot(symbol="ADAUSDT")
