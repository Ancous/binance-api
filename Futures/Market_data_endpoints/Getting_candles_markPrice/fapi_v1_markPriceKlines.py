import requests
import json


def get_candles_markprice(symbol: str,
                          interval: str,
                          start_time: str = None,
                          end_time: str = None,
                          limit: str = "500") -> dict:

    """
    Запрос:
    Получить информацию по свечам для Mark Price

    Полный url:
    "https://fapi.binance.com/fapi/v1/indexPriceKlines"

    Вес запроса:
    [[limits: вес], [1-100: 1], [101-500: 2], [501-1000: 5], [1001-1500: 10]]

    Параметры:
    - symbol="pair" (str): актив ("BTCUSDT", ...)
    - interval="interval" (str): интервал свечи ("1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M")
    - start_time="startTime" (str):  время начала отбора ("1681505080619", ...)
    - end_time="endTime" (str): время окончания отбора ("1681505034619", ...)
    - limit="limit" (str): количество выводимых заявок в стакане в одну сторону ("1", ..., "1500")

    Комментарии:
    - сокращения "interval": [m -> минута; h -> час; d -> день; w -> неделя; M -> месяц]
    - Если startTime и endTime не отправлены, возвращаются самые последние klines.

    Ответ:
    [
       [
          1683106200000,   (время открытие свечи)
          "0.38511536",   (цена открытия свечи)
          "0.38538294",   (самая высокая цена свечи)
          "0.38491268",   (самая низкая цена свечи)
          "0.38527970",   (цена закрытия свечи (или последняя цена))
          "0",   (Ignore)
          1683106499999,   (время закрытие свечи)
          "0",   (Ignore)
          300,   (Ignore)
          "0",   (Ignore)
          "0",   (Ignore)
          "0"   (Ignore)
       ],
       [
          1683106500000,   (время открытие свечи)
          "0.38527972",   (цена открытия свечи)
          "0.38536943",   (самая высокая цена свечи)
          "0.38512590",   (самая низкая цена свечи)
          "0.38531733",   (цена закрытия свечи (или последняя цена))
          "0",   (Ignore)
          1683106799999,   (время закрытие свечи)
          "0",   (Ignore)
          192,   (Ignore)
          "0",   (Ignore)
          "0",   (Ignore)
          "0"   (Ignore)
       ]
    ]
    """

    # ---------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/indexPriceKlines"
    parameters = {
        "pair": symbol.upper(),
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

    result_2 = get_candles_markprice(symbol="ADAUSDT", interval="1m")

    if result_2["status_code"] == 200:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("result:", result_2["result"])
    else:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("code_error:", result_2["code_error"])
        print("text_error:", result_2["text_error"])
