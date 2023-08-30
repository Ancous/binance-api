import json
import requests


def get_candles_blvt_nav(symbol: str,
                         interval: str,
                         start_time: str = None,
                         end_time: str = None,
                         limit: str = "500") -> dict:

    """
    Запрос:
    Получить информацию по историческим свечам BLVT NAV

    Полный url:
    "https://fapi.binance.com/fapi/v1/lvtKlines"

    Вес запроса:
    5

    Параметры:
    - symbol="symbol" (str): актив ("BTCDOWN", ...)
    - interval="interval" (str): интервал свечи ("1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M")
    - start_time="startTime" (str):  время начала отбора ("1681505080619", ...)
    - end_time="endTime" (str): время окончания отбора ("1681505034619", ...)
    - limit="limit" (str): какое количество свечей вывести ("1", ..., "1000")

    Комментарии:
    - сокращения "interval": [m -> минута; h -> час; d -> день; w -> неделя; M -> месяц]
    - Рыночные сделки означают сделки, заполненные в книге заявок.
    - Будут возвращены только рыночные сделки, это означает, что сделки страхового фонда и сделки ADL не будут возвращены.

    Ответ:
    [
        [
            1598371200000,  (время открытия)
            "5.88275270",   (цена открытая цена NAV)
            "6.03142087",   (самая высокая цена NAV)
            "5.85749741",   (самая низкая цена NAV)
            "5.99403551",   (цена закрытия NAV (или последняя))
            "2.28602984",   (реальное кредитное плечо)
            1598374799999,   (время закрытия)
            "0",   (Ignore)
            6209,   (Количество обновлений NAV)
            "14517.64507907",   (Ignore)
            "0",   (Ignore)
            "0"   (Ignore)
        ]
    ]
    """
    
    # ---------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/lvtKlines"
    parameters = {
        "symbol": symbol.upper(),
        "interval": interval,
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

    result_2 = get_candles_blvt_nav(symbol="BTCDOWN", interval="1m")

    if result_2["status_code"] == 200:
        print("status_code:" ,result_2["status_code"])
        print("headers:", result_2["headers"])
        print("result:", result_2["result"])
    else:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("code_error:", result_2["code_error"])
        print("text_error:", result_2["text_error"])
