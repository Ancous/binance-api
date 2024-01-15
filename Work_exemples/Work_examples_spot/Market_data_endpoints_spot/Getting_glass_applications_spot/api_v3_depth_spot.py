import requests
import json


def get_glass_applications_spot(symbol: str,
                                limit: str = "100") -> dict:

    """
    Запрос:
    Получить стакан заявок спота

    Полный url:
    "https://api.binance.com/api/v3/depth"

    Вес запроса:
    [[limits: вес], [1-100: 2], [101-500: 10], [501-1000: 20], [1001-5000: 100]]

    Параметры:
    - symbol="symbol" (str): актив ("BTCUSDT", ...)
    - limit="limit" (str): количество выводимых заявок в стакане в одну сторону ("1", ..., "5000")

    Комментарии:
    - None

    Ответ:
    {
       "lastUpdateId": 7373908556,
       "bids": [
          [
             "0.27310000",
             "53080.10000000"
          ],
          [
             "0.27300000",
             "72853.80000000"
          ]
       ],
       "asks": [
          [
             "0.27320000",
             "19046.20000000"
          ],
          [
             "0.27330000",
             "84362.00000000"
          ]
       ]
    }
    """

    # ---------------------------------------------
    base_url = "https://api.binance.com"
    end_point = "/api/v3/depth"
    parameters = {
        "symbol": symbol.upper(),
        "limit": limit
    }
    # ---------------------------------------------

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

    get_glass_applications_spot(symbol="ADAUSDT", limit="2")
