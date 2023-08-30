import requests
import time
import json
import os
import hmac
import hashlib
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()


def get_update_order_history(symbol: str,
                             time_stamp: str,
                             start_time: str = "",
                             end_time: str = "",
                             order_id: str = "",
                             orig_client_order_id: str = "",
                             limit: str = "50",
                             recv_window: str = "5000") -> dict:

    """
    Запрос:
    Получить историю изменений ордеров

    Полный url:
    "https://fapi.binance.com/fapi/v1/orderAmendment"

    Вес запроса:
    1

    Параметры:
    - symbol="symbol" (str): актив ("BTCUSDT", ...)
    - time_stamp="timestamp" (str): время отправки запроса ("1681501516492", ...)
    - start_time="startTime" (str): время начала отбора ("1681505080619", ...)
    - end_time="endTime" (str): время окончания отбора ("1681505034619", ...)
    - order_id="orderId" (str): самозаполняющимся идентификатор для каждой сделки ("567834287", ...)
    - orig_client_order_id="origClientOrderId" (str): идентификатор сделки  ("567887", ...)
    - limit="limit" (str): какое количество вывести ("5", ..., "500")
    - recv_window="recvWindow" (str): количество миллисекунд, в течение которых запрос действителен ("1000", ..., "70000")

    Комментарии:
    - Необходимо обязательно отправить либо order_id, либо orig_client_order_id.
    - orderId имеет преимущественную силу, если отправлены оба.

    Ответ:
    [
       {
          "amendmentId": 51045853,
          "symbol": "ADAUSDT",
          "pair": "ADAUSDT",
          "orderId": 32717797178,
          "clientOrderId": "74707",
          "time": 1686134330452,
          "amendment": {
             "price": {
                "before": "0.33000",
                "after": "0.31000"
             },
             "origQty": {
                "before": "17",
                "after": "68"
             },
             "count": 1
          }
       }
    ]
    """

    # -------------------------------------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/orderAmendment"
    api_key = os.getenv("api_key")
    secret_key = os.getenv("secret_key")
    parameters = {
        "symbol": symbol.upper(),
        "timestamp": time_stamp,
        "startTime": start_time,
        "endTime": end_time,
        "orderId": order_id,
        "origClientOrderId": orig_client_order_id,
        "limit": limit,
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

    result_2 = get_update_order_history(symbol="ADAUSDT", time_stamp=str(round(time.time() * 1000)), order_id="32717797177", orig_client_order_id="14019")

    if result_2["status_code"] == 200:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("result:", result_2["result"])
    else:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("code_error:", result_2["code_error"])
        print("text_error:", result_2["text_error"])
