import requests
import json


def get_glass_applications(symbol: str,
                           limit: str = "500") -> dict:

    """
    Запрос:
    Получить стакан заявок

    Полный url:
    "https://fapi.binance.com/fapi/v1/depth"

    Вес запроса:
    [[limits: вес], [5, 10, 20, 50: 2], [100: 5], [500: 10], [1000: 20]]

    Параметры:
    - symbol="symbol" (str): актив ("BTCUSDT", ...)
    - limit="limit" (str): количество выводимых заявок в стакане в одну сторону ("5", "10", "20", "50", "100", "500", "1000")

    Комментарии:
    - None

    Ответ:
    {
       "lastUpdateId": 2740723675122,
       "E": 1681512613548,  (Время вывода сообщения)
       "T": 1681512613528,  (Время транзакции)
       "bids": [
          [
             "0.43920",  (цена)
             "18403"  (количество)
          ],
          [
             "0.43910",
             "120359"
          ],
          [
             "0.43900",
             "105792"
          ],
          [
             "0.43890",
             "98038"
          ],
          [
             "0.43880",
             "234323"
          ]
       ],
       "asks": [
          [
             "0.43930",
             "82740"
          ],
          [
             "0.43940",
             "90407"
          ],
          [
             "0.43950",
             "186146"
          ],
          [
             "0.43960",
             "115142"
          ],
          [
             "0.43970",
             "127414"
          ]
       ]
    }
    """

    # ---------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/depth"
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
        return {"status_code": response.status_code, "headers": response.headers, "result": result}
    else:
        return {"status_code": response.status_code, "headers": response.headers, "code_error": result['code'], "text_error": result['msg']}


if __name__ in "__main__":

    result_2 = get_glass_applications(symbol="ADAUSDT")

    if result_2["status_code"] == 200:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("result:", result_2["result"])
    else:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("code_error:", result_2["code_error"])
        print("text_error:", result_2["text_error"])
