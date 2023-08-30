import requests
import json


def get_history_funding_rate(symbol: str = "",
                             start_time: str = None,
                             end_time: str = None,
                             limit: str = "500") -> dict:

    """
    Запрос:
    Получить историю ставок финансирования

    Полный url:
    "https://fapi.binance.com/fapi/v1/fundingRate"

    Вес запроса:
    None

    Параметры:
    - symbol="symbol" (str): актив ("BTCUSDT", ...)
    - start_time="startTime" (str):  время начала отбора ("1681505080619", ...)
    - end_time="endTime" (str): время окончания отбора ("1681505034619", ...)
    - limit="limit" (str): количество выводимых заявок в стакане в одну сторону ("1", ..., "1000")

    Комментарии:
    - Если "startTime" и "endTime" не отправлены, возвращаются самые последние данные лимита.

    Ответ:
    [
       {
          "symbol": "ADAUSDT",
          "fundingTime": 1683273600000,
          "fundingRate": "0.00010000"
       },
       {
          "symbol": "ADAUSDT",
          "fundingTime": 1683302400000,
          "fundingRate": "0.00010000"
       }
    ]
    """

    # ------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/fundingRate"
    parameters = {
        "symbol": symbol.upper(),
        "limit": limit,
        "startTime": start_time,
        "endTime": end_time
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

    result_2 = get_history_funding_rate()

    if result_2["status_code"] == 200:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("result:", result_2["result"])
    else:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("code_error:", result_2["code_error"])
        print("text_error:", result_2["text_error"])
