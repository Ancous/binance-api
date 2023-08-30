import requests
import json


def get_current_open_interest(symbol: str) -> dict:

    """
    Запрос:
    Получить текущий открытый интерес

    Полный url:
    "https://fapi.binance.com/fapi/v1/openInterest"

    Вес запроса:
    1

    Параметры:
    - symbol="symbol" (str): актив ("BTCUSDT", ...)

    Комментарии:
    - None

    Ответ:
    {
       "symbol": "ADAUSDT",
       "openInterest": "197547968",
       "time": 1683302122501
    }
    """

    # ------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/openInterest"
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

    result_2 = get_current_open_interest(symbol="ADAUSDT")

    if result_2["status_code"] == 200:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("result:", result_2["result"])
    else:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("code_error:", result_2["code_error"])
        print("text_error:", result_2["text_error"])
