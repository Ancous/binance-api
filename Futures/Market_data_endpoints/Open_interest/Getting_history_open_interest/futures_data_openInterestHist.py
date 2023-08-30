import requests
import json


def get_historical_open_interest(symbol: str,
                                 period: str,
                                 start_time: str = None,
                                 end_time: str = None,
                                 limit: str = "500") -> dict:

    """
    Запрос:
    Получить историю открытого интереса

    Полный url:
    "https://fapi.binance.com/futures/data/openInterestHist"

    Вес запроса:
    None

    Параметры:
    - symbol="symbol" (str): актив ("BTCUSDT", ...)
    - period="period" (str): период для высчитывания ("5m", "15m", "30m", "1h", "2h", "4h", "6h", "12h", "1d")
    - start_time="startTime" (str):  время начала отбора ("1681505080619", ...)
    - end_time="endTime" (str): время окончания отбора ("1681505034619", ...)
    - limit="limit" (str): количество выводимых заявок в стакане в одну сторону ("1", ..., "1500")

    Комментарии:
    - Если startTime и endTime не отправлены, возвращаются самые последние данные.
    - Доступны только данные за последние 30 дней.

    Ответ:
    [
       {
          "symbol": "ADAUSDT",
          "sumOpenInterest": "196816286.00000000",   (общий открытый интерес)
          "sumOpenInterestValue": "77093214.76900040",   (общая стоимость открытого интереса)
          "timestamp": 1683300600000
       },
       {
          "symbol": "ADAUSDT",
          "sumOpenInterest": "196952337.00000000",   (общий открытый интерес)
          "sumOpenInterestValue": "77205316.10400000",   (общая стоимость открытого интереса)
          "timestamp": 1683300900000
       }
    ]
    """

    # ------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/futures/data/openInterestHist"
    parameters = {
        "symbol": symbol.upper(),
        "period": period,
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

    result_2 = get_historical_open_interest(symbol="ADAUSDT", period="5m")

    if result_2["status_code"] == 200:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("result:", result_2["result"])
    else:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("code_error:", result_2["code_error"])
        print("text_error:", result_2["text_error"])
