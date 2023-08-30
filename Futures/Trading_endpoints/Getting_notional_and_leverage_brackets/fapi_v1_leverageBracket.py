import requests
import time
import json
import os
import hmac
import hashlib
from urllib.parse import urlencode
from dotenv import load_dotenv


load_dotenv()


def get_nl_brackets(time_stamp: str,
                    symbol: str = "",
                    recv_window: str = "5000") -> dict:
  
    """
    Запрос:
    ???

    Полный url:
    "https://fapi.binance.com/fapi/v1/leverageBracket"

    Вес запроса:
    1

    Параметры:
    - time_stamp="timestamp" (str): время отправки запроса ("1681501516492", ...)
    - symbol="symbol" (str): актив ("BTCUSDT", ...)
    - recv_window="recvWindow" (str): количество миллисекунд, в течение которых запрос действителен ("1000", ..., "70000")

    Комментарии:
    - None

    Ответ:
    [
       {
          "symbol": "ADAUSDT",
          "brackets": [
             {
                "bracket": 1,   (условная скобка)
                "initialLeverage": 75,   (Максимальное начальное кредитное плечо для этой группы)
                "notionalCap": 5000,   (Ограничение условного обозначения этой скобки)
                "notionalFloor": 0,   (Условный порог этой скобки)
                "maintMarginRatio": 0.005,   (Коэффициент поддержки для этой группы)
                "cum": 0.0   (Вспомогательное число для быстрого расчета)
             },
             {...},
             {...},
             {...},
             {...},
             {...},
             {...},
             {...},
             {...},
             {...}
          ]
       }
    ]
    """

    # -------------------------------------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/leverageBracket"
    api_key = os.getenv("api_key")
    secret_key = os.getenv("secret_key")
    parameters = {
        "symbol": symbol.upper(),
        "timestamp": time_stamp,
        "recvWindow": recv_window
    }
    query_string = urlencode(parameters)
    parameters["signature"] = hmac.new(key=secret_key.encode(),
                                       msg=query_string.encode(),
                                       digestmod=hashlib.sha256).hexdigest()
    # -------------------------------------------------------------------------

    complete_request = base_url + end_point
    complete_parameters = parameters
    headers = {
        "X-MBX-APIKEY": api_key
    }

    response = requests.get(url=complete_request, params=complete_parameters, headers=headers)
    result = json.loads(response.text)
    
    if response.status_code == 200:
        with open("answer.json", "w") as file:
            json.dump(obj=result, fp=file, indent=3)
        return {"status_code": response.status_code, "headers": response.headers, "result": result}
    else:
        return {"status_code": response.status_code, "headers": response.headers, "code_error": result['code'], "text_error": result['msg']}


if __name__ in "__main__":

    result_2 = get_nl_brackets(time_stamp=str(round(time.time() * 1000)))

    if result_2["status_code"] == 200:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("result:", result_2["result"])
    else:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("code_error:", result_2["code_error"])
        print("text_error:", result_2["text_error"])
