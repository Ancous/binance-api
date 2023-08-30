import requests
import json


def get_ratio_long_short_account(symbol: str,
                                 period: str,
                                 start_time: str = None,
                                 end_time: str = None,
                                 limit: str = "30") -> dict:

    """
    Запрос:
    Получить общее соотношение количества длинных/коротких счетов

    Полный url:
    "https://fapi.binance.com/futures/data/globalLongShortAccountRatio"

    Вес запроса:
    None

    Параметры:
    - symbol="symbol" (str): актив ("BTCUSDT", ...)
    - period="period" (str): период для высчитывания ("5m", "15m", "30m", "1h", "2h", "4h", "6h", "12h", "1d")
    - start_time="startTime" (str):  время начала отбора ("1681505080619", ...)
    - end_time="endTime" (str): время окончания отбора ("1681505034619", ...)
    - limit="limit" (str): количество выводимых заявок в стакане в одну сторону ("1", ..., "500")

    Комментарии:
    - Если startTime и endTime не отправлены, возвращаются самые последние данные.
    - Доступны только данные за последние 30 дней.

    Ответ:
    [
       {
          "symbol": "ADAUSDT",
          "longAccount": "0.7525",   (общее соотношение количества длинных счетов)
          "longShortRatio": "3.0404",   (общее соотношение количества длинных/коротких счетов)
          "shortAccount": "0.2475",   (общее соотношение количества коротких счетов)
          "timestamp": 1683297300000
       },
       {
          "symbol": "ADAUSDT",
          "longAccount": "0.7497",   (общее соотношение количества длинных счетов)
          "longShortRatio": "2.9952",   (общее соотношение количества длинных/коротких счетов)
          "shortAccount": "0.2503",   (общее соотношение количества коротких счетов)
          "timestamp": 1683297600000
       }
    ]
    """

    # ------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/futures/data/globalLongShortAccountRatio"
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

    result_2 =get_ratio_long_short_account(symbol="ADAUSDT", period="5m")

    if result_2["status_code"] == 200:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("result:", result_2["result"])
    else:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("code_error:", result_2["code_error"])
        print("text_error:", result_2["text_error"])
