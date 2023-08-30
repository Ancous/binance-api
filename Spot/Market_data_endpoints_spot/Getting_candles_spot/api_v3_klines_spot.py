import requests
import json


def get_candles_spot(symbol: str,
                     interval: str,
                     start_time: str = None,
                     end_time: str = None,
                     limit: str = "500") -> dict:

    """
    Запрос:
    Получить информацию по свечам спота

    Полный url:
    "https://api.binance.com/api/v3/klines"

    Вес запроса:
    1

    Параметры:
    - symbol="symbol" (str): актив ("BTCUSDT", ...)
    - interval="interval" (str): интервал свечи ("1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M")
    - start_time="startTime" (str):  время начала отбора ("1681505080619", ...)
    - end_time="endTime" (str): время окончания отбора ("1681505034619", ...)
    - limit="limit" (str): какое количество свечей вывести ("1", ..., "1000")

    Комментарии:
    - сокращения "interval": [m -> минута; h -> час; d -> день; w -> неделя; M -> месяц]
    - Если "startTime" и "endTime" не отправлены, возвращаются самые последние klines.

    Ответ:
    [
        [
            1681748820000,   (время открытие свечи)
            "29352.00",   (цена открытия свечи)
            "29385.00",   (самая высокая цена свечи)
            "29351.90",   (самая низкая цена свечи)
            "29385.00",   (цена закрытия свечи (или последняя цена))
            "414.755",   (объем в свече)
            1681748879999,   (время закрытия свечи)
            "12180316.04890",   (объем котируемого актива)
            3226,   (сделок в свече)
            "303.985",   (Taker buy base asset volume)
            "8926873.01530",   (Taker buy quote asset volume)
            "0"   (Ignore)
        ],
        [
            1681748880000,
            "29385.00",
            "29385.00",
            "29379.30",
            "29381.30",
            "65.643",
            1681748939999,
            "1928766.40370",
            729,
            "41.395",
            "1216276.73170",
            "0"
        ]
    ]
    """

    # ---------------------------------------------
    base_url = "https://api.binance.com"
    end_point = "/api/v3/klines"
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
        return {"status_code": response.status_code, "result": result}
    else:
        return {"status_code": response.status_code, "code_error": result['code'], "text_error": result['msg']}


if __name__ in "__main__":

    get_candles_spot(symbol="ADAUSDT", interval="5m")
