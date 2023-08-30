import requests
import json
import time
import os
import hmac
import hashlib
from urllib.parse import urlencode
from dotenv import load_dotenv


load_dotenv()


def delete_multiple_orders_time(symbol: str,
                                countdown_time: str,
                                time_stamp: str,
                                recv_window: str = "5000") -> dict:
  
    """
    Запрос:
    Закрыть все ордера по символу через заданное время

    Полный url:
    "https://fapi.binance.com/fapi/v1/countdownCancelAll"

    Вес запроса:
    0

    Параметры:
    - symbol="symbol" (str): актив ("BTCUSDT", ...)
    - countdown_time="countdownTime" (str): количество миллисекунд до закрытия ордеров ("54000", ...)
    - time_stamp="timestamp" (str): время отправки запроса ("1681501516492", ...)
    - recv_window="recvWindow" (str): количество миллисекунд, в течение которых запрос действителен ("1000", ..., "70000")

    Комментарии:
    - countdown_time задается в миллисекундах
    - Закрывает ордера, не открытые позиции!!!

    Ответ:
    {
       "symbol": "ADAUSDT",
       "countdownTime": "20000"
    }
    """

    # -------------------------------------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/countdownCancelAll"
    api_key = os.getenv("api_key")
    secret_key = os.getenv("secret_key")
    parameters = {
        "symbol": symbol.upper(),
        "countdownTime": countdown_time,
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

    response = requests.post(url=complete_request, data=complete_parameters, headers=headers)
    result = json.loads(response.text)
    
    if response.status_code == 200:
        with open("answer.json", "w") as file:
            json.dump(obj=result, fp=file, indent=3)
        return {"status_code": response.status_code, "result": result}
    else:
        return {"status_code": response.status_code, "code_error": result['code'], "text_error": result['msg']}


if __name__ in "__main__":

    delete_multiple_orders_time(symbol="ADAUSDT", countdown_time="20000", time_stamp=str(round(time.time() * 1000)))
