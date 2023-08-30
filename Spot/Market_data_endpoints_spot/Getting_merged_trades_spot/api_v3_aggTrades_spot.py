import requests
import json


def get_merged_trades_spot(symbol: str,
                           from_id: str = None,
                           start_time: str = None,
                           end_time: str = None,
                           limit: str = "500") -> dict:

    """
    Запрос:
    Получить объединенные сделки спота

    Полный url:
    "https://api.binance.com/api/v3/aggTrades"

    Вес запроса:
    1

    Параметры:
    - symbol="symbol" (str): актив ("BTCUSDT", ...)
    - from_id="fromId": (str): идентификатор объединенной сделки от которой будет произведён вывод следующих объединенных сделок ("567887", ...)
    - start_time="startTime" (str):  время начала отбора ("1681505080619", ...)
    - end_time="endTime" (str): время окончания отбора ("1681505034619", ...)
    - limit="limit" (str): какое количество объединенных сделок вывести ("1", ..., "1000")

    Комментарии:
    - Рыночные сделки, которые занимают 100 мс с одной и той же ценой и одной и той же стороной, будут иметь агрегированное количество.
    - Если отправлены и "startTime", и "endTime", время между "startTime" и "endTime" должно быть меньше 1 часа.
    - Если "fromId", "startTime" и "endTime" не отправлены, будут возвращены самые последние совокупные сделки.
    - Только рыночные сделки будут объединены и возвращены, что означает, что сделки страхового фонда и сделки ADL не будут объединены.
    - Отправка как "startTime"/"endTime", так и "fromId" может привести к тайм-ауту ответа, отправьте либо "fromId", либо "startTime"/"endTime"

    Ответ:
    [
        {
          "a": 1694766796,  (ID сделки)
          "p": "29438.90",  (цена)
          "q": "0.004",  (объем)
          "f": 3576795159,  (ID первой сделки)
          "l": 3576795159,  (ID последней сделки)
          "T": 1681744105358,  (время)
          "m": true  (совершена ли сделка по market trades)
        },
        {
          "a": 1694766797,
          "p": "29439.00",
          "q": "0.067",
          "f": 3576795160,
          "l": 3576795160,
          "T": 1681744105365,
          "m": false
        }
    ]
    """

    # ---------------------------------------------
    base_url = "https://api.binance.com"
    end_point = "/api/v3/aggTrades"
    parameters = {
        "symbol": symbol.upper(),
        "limit": limit,
        "fromId": from_id,
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

    get_merged_trades_spot(symbol="ADAUSDT")
