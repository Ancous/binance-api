import requests
import time
import json
import os
import hmac
import hashlib
from urllib.parse import urlencode
from dotenv import load_dotenv


load_dotenv()


def get_income_history(time_stamp: str,
                       symbol: str = "",
                       income_type: str = "",
                       start_time: str = "",
                       end_time: str = "",
                       limit: str = "100",
                       recv_window: str = "5000") -> dict:
  
    """
    Запрос:
    Получить историю доходов

    Полный url:
    "https://fapi.binance.com/fapi/v1/income"

    Вес запроса:
    30

    Параметры:
    - time_stamp="timestamp" (str): время отправки запроса ("1681501516492", ...)
    - symbol="symbol" (str): актив ("BTCUSDT", ...)
    - income_type="incomeType" (str): тип дохода (	"TRANSFER", "WELCOME_BONUS", "REALIZED_PNL", "FUNDING_FEE", "COMMISSION", "INSURANCE_CLEAR", "REFERRAL_KICKBACK", "COMMISSION_REBATE", "API_REBATE", "CONTEST_REWARD", "CROSS_COLLATERAL_TRANSFER", "OPTIONS_PREMIUM_FEE", "OPTIONS_SETTLE_PROFIT", "INTERNAL_TRANSFER", "AUTO_EXCHANGE", "DELIVERED_SETTELMENT", "COIN_SWAP_DEPOSIT", "COIN_SWAP_WITHDRAW", "POSITION_LIMIT_INCREASE_FEE")
    - start_time="startTime" (str): время начала отбора ("1681505080619", ...)
    - end_time="endTime" (str): время окончания отбора ("1681505034619", ...)
    - limit="limit" (str): какое количество сделок (информация о доходе) вывести ("5", ..., "1000")
    - recv_window="recvWindow" (str): количество миллисекунд, в течение которых запрос действителен ("1000", ..., "70000")

    Комментарии:
    - Если "startTime" и "endTime" не отправлены, будут возвращены данные за последние 7 дней.
    - Если не передан "incomeType", будут возвращены все виды дохода.
    - История доходов содержит данные только за последние три месяца.

    Ответ:
    [
       {
          "symbol": "ADAUSDT",   (торговый символ, если он есть)
          "incomeType": "REALIZED_PNL",   (тип дохода)
          "income": "0.01680000",   (сумма дохода)
          "asset": "USDT",   (доходный актив)
          "time": 1682287762000,
          "info": "910576696",   (дополнительная информация)
          "tranId": 90241910576696,   (идентификатор транзакции)
          "tradeId": "910576696"   (идентификатор сделки, если он есть)
       },
       {
          "symbol": "ADAUSDT",
          "incomeType": "COMMISSION",
          "income": "-0.00644448",
          "asset": "USDT",
          "time": 1682287762000,
          "info": "910576696",
          "tranId": 90241910576696,
          "tradeId": "910576696"
       }
    ]
    """

    # -------------------------------------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/income"
    api_key = os.getenv("api_key")
    secret_key = os.getenv("secret_key")
    parameters = {
        "timestamp": time_stamp,
        "symbol": symbol.upper(),
        "incomeType": income_type,
        "startTime": start_time,
        "endTime": end_time,
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

    result_2 = get_income_history(time_stamp=str(round(time.time() * 1000)))

    if result_2["status_code"] == 200:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("result:", result_2["result"])
    else:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("code_error:", result_2["code_error"])
        print("text_error:", result_2["text_error"])
