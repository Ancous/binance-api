import requests
import json


def get_average_price_spot(symbol: str) -> dict:

    """
    Запрос:
    Получить текущею среднюю цену символа спота

    Полный url:
    "https://api.binance.com/api/v3/avgPrice"

    Вес запроса:
    2

    Параметры:
    - symbol="symbol" (str): актив ("BTCUSDT", ...)

    Комментарии:
    - None

    Ответ:
    {
       "mins": 5,
       "price": "0.27282934"
    }
    """

    # ------------------------------------------
    base_url = "https://api.binance.com"
    end_point = "/api/v3/avgPrice"
    parameters = {
        "symbol": symbol.upper(),
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

    get_average_price_spot(symbol="ADAUSDT")
