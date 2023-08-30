import requests
import time
import json
import os
import hmac
import hashlib
from urllib.parse import urlencode
from dotenv import load_dotenv


load_dotenv()


def get_balance_account(time_stamp: str,
                        recv_window: str = "5000") -> dict:
  
    """
    Запрос:
    Получить баланс фьючерсного счета

    Полный url:
    "https://fapi.binance.com/fapi/v2/balance"

    Вес запроса:
    5

    Параметры:
    - time_stamp="timestamp" (str): время отправки запроса ("1681501516492", ...)
    - recv_window="recvWindow" (str): количество миллисекунд, в течение которых запрос действителен ("1000", ..., "70000")

    Комментарии:
    - None
    
    Ответ:
    [
        {
            "accountAlias": "FzSguXAumYAumY",   (уникальный код счета)
            "asset": "ETH",   (имя актива)
            "balance": "0.00000000",   (баланс актива)
            "crossWalletBalance": "0.00000000",   (сокращённый баланс актива)
            "crossUnPnl": "0.00000000",   (нереализованная прибыль пересеченных позиций)
            "availableBalance": "0.00000000",   (доступные средства)
            "maxWithdrawAmount": "0.00000000",   (максимальная сумма для перевода)
            "marginAvailable": true,   (можно ли использовать актив в качестве маржи в режиме Multi-Assets)
            "updateTime": 0   (последние время взаимодействия с ордером)
        },
        {
            "accountAlias": "FzSguXAumYAumY",   (уникальный код счета)
            "asset": "USDT",   (имя актива)
            "balance": "86.87857855",   (баланс актива)
            "crossWalletBalance": "86.87857855",   (сокращённый баланс актива)
            "crossUnPnl": "0.00000000",   (нереализованная прибыль пересеченных позиций)
            "availableBalance": "86.87857855",   (доступные средства)
            "maxWithdrawAmount": "86.87857855",   (максимальная сумма для перевода)
            "marginAvailable": true,   (можно ли использовать актив в качестве маржи в режиме Multi-Assets)
            "updateTime": 1682009841851   (последние время взаимодействия с ордером)
        }
    ]
    """

    # -------------------------------------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v2/balance"
    api_key = os.getenv("api_key")
    secret_key = os.getenv("secret_key")
    parameters = {
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

    result_2 = get_balance_account(time_stamp=str(round(time.time() * 1000)))

    if result_2["status_code"] == 200:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("result:", result_2["result"])
    else:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("code_error:", result_2["code_error"])
        print("text_error:", result_2["text_error"])
