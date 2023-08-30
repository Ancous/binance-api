import requests
import json


def get_day_statistics(symbol: str = "") -> dict:

    """
    Запрос:
    Получить статистику изменения цены за 24 часа

    Полный url:
    "https://fapi.binance.com/fapi/v1/ticker/24hr"

    Вес запроса:
    1 для одного символа, 40 когда параметр символа отсутствует

    Параметры:
    - symbol="symbol" (str): актив ("BTCUSDT", ...)

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
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/ticker/24hr"
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
        return {"status_code": response.status_code, "headers": response.headers, "result": result}
    else:
        return {"status_code": response.status_code, "headers": response.headers, "code_error": result['code'], "text_error": result['msg']}


if __name__ in "__main__":

    result_2 = get_day_statistics()

    if result_2["status_code"] == 200:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("result:", result_2["result"])
    else:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("code_error:", result_2["code_error"])
        print("text_error:", result_2["text_error"])
