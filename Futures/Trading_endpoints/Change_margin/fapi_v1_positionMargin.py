import requests
import json
import time
import os
import hmac
import hashlib
from urllib.parse import urlencode
from dotenv import load_dotenv


load_dotenv()


def post_margin(symbol: str,
                amount: str,
                my_type: str,
                time_stamp: str,
                position_side: str = "BOTH",
                recv_window: str = "5000") -> dict:
  
    """
    Запрос:
    Изменить количество маржи изолированной позиции

    Полный url:
    "https://fapi.binance.com/fapi/v1/positionMargin"

    Вес запроса:
    1

    Параметры:
    - symbol="symbol" (str): актив ("BTCUSDT", ...)
    - amount="amount" (str): количество добавленной или убранной маржи ("65", ...)
    - my_type="type" (str): что делать с маржой ("1", "2")
    - time_stamp="timestamp" (str): время отправки запроса ("1681501516492", ...)
    - position_side="positionSide" (str): ... ("BOTH", "LONG", "SHORT")
    - recv_window="recvWindow" (str): количество миллисекунд, в течение которых запрос действителен ("1000", ..., "70000")

    Комментарии:
    - Работает только для изолированного актива
    - "type" возможные варианты: [1 - добавить маржу позиции, 2 - уменьшить маржу позиции]

    Ответ:
    {
       "code": 200,
       "msg": "Successfully modify position margin.",
       "amount": 5.0,
       "type": 1
    }
    """

    # -------------------------------------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/positionMargin"
    api_key = os.getenv("api_key")
    secret_key = os.getenv("secret_key")
    parameters = {
        "symbol": symbol.upper(),
        "amount": amount,
        "type": my_type,
        "positionSide": position_side,
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
        return {"status_code": response.status_code, "headers": response.headers, "result": result}
    else:
        return {"status_code": response.status_code, "headers": response.headers, "code_error": result['code'], "text_error": result['msg']}


if __name__ in "__main__":

    result_2 = post_margin(symbol="ADAUSDT", amount="1", my_type="2", time_stamp=str(round(time.time() * 1000)))

    if result_2["status_code"] == 200:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("result:", result_2["result"])
    else:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("code_error:", result_2["code_error"])
        print("text_error:", result_2["text_error"])
