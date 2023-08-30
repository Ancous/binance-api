import requests
import time
import json
import os
import hmac
import hashlib
from urllib.parse import urlencode
from dotenv import load_dotenv


load_dotenv()


def get_margin_change_history(symbol: str,
                              time_stamp: str,
                              my_type: str = "",
                              start_time: str = "",
                              end_time: str = "",
                              limit: str = "500",
                              recv_window: str = "5000") -> dict:
  
    """
    Запрос:
    Получить историю изменения маржи

    Полный url:
    "https://fapi.binance.com/fapi/v1/positionMargin/history"

    Вес запроса:
    1

    Параметры:
    - symbol="symbol" (str): актив ("BTCUSDT", ...)
    - time_stamp="timestamp" (str): время отправки запроса ("1681501516492", ...)
    - my_type="type" (str): какое действие с маржой показывать ("1", "2")
    - start_time="startTime" (str): время начала отбора ("1681505080619", ...)
    - end_time="endTime" (str): время окончания отбора ("1681505034619", ...)
    - limit="limit" (str): какое количество вывести ("5", ..., "1000")
    - recv_window="recvWindow" (str): количество миллисекунд, в течение которых запрос действителен ("1000", ..., "70000")

    Комментарии:
    - "type" возможные варианты: [1 - показать добавление маржи, 2 - показать уменьшение маржи]

    Ответ:
    [
       {
          "symbol": "ADAUSDT",
          "type": 1,
          "deltaType": "TRADE",
          "amount": "4.04422425",
          "asset": "USDT",
          "time": 1606982998900,
          "positionSide": "BOTH",
          "clientTranId": ""
       },
       {
          "symbol": "ADAUSDT",
          "type": 2,
          "deltaType": "TRADE",
          "amount": "-4.04422425",
          "asset": "USDT",
          "time": 1606983593938,
          "positionSide": "BOTH",
          "clientTranId": ""
       }
    ]
    """

    # -------------------------------------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/positionMargin/history"
    api_key = os.getenv("api_key")
    secret_key = os.getenv("secret_key")
    parameters = {
        "symbol": symbol.upper(),
        "type": my_type,
        "startTime": start_time,
        "endTime": end_time,
        "limit": limit,
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

    result_2 = get_margin_change_history(symbol="ADAUSDT", time_stamp=str(round(time.time() * 1000)))

    if result_2["status_code"] == 200:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("result:", result_2["result"])
    else:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("code_error:", result_2["code_error"])
        print("text_error:", result_2["text_error"])
