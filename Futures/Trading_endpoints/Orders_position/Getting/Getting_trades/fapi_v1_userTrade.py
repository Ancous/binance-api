import requests
import time
import json
import os
import hmac
import hashlib
from urllib.parse import urlencode
from dotenv import load_dotenv


load_dotenv()


def get_trades(symbol: str,
               time_stamp: str,
               order_id: str = "",
               start_time: str = "",
               end_time: str = "",
               from_id: str = "",
               limit: str = "500",
               recv_window: str = "5000") -> dict:
  
    """
    Запрос:
    Получить информацию о сделках

    Полный url:
    "https://fapi.binance.com/fapi/v1/userTrades"

    Вес запроса:
    5

    Параметры:
    - symbol="symbol" (str): актив ("BTCUSDT", ...)
    - time_stamp="timestamp" (str): время отправки запроса ("1681501516492", ...)
    - order_id="orderId" (str): самозаполняющимся идентификатор для каждой сделки ("567834287", ...)
    - start_time="startTime" (str): время начала отбора ("1681505080619", ...)
    - end_time="endTime" (str): время окончания отбора ("1681505034619", ...)
    - from_id="fromId" (str): ... ("567834287", ...)
    - limit="limit" (str): какое количество ордеров вывести ("5", ..., "1000")
    - recv_window="recvWindow" (str): количество миллисекунд, в течение которых запрос действителен ("1000", ..., "70000")

    Комментарии:
    - "orderId" является самозаполняющимся для каждого конкретного символа
    - "fromId" является "id" в ответе.
    - Если использовать "fromId" то будут выводиться сделки от "fromId" включительно
    - Если "startTime" и "endTime" не отправлены, будут возвращены данные за последние 7 дней.
    - Период между "startTime" и  "endTime" должен быть меньше 7 дней (по умолчанию последние 7 дней).
    - Параметр "fromId" нельзя отправлять с "startTime" или "endTime".

    Ответ:
    [
       {
          "symbol": "ADAUSDT",
          "id": 910559362,
          "orderId": 31479414461,
          "side": "SELL",
          "price": "0.38400",
          "qty": "14",
          "realizedPnl": "0",
          "marginAsset": "USDT",
          "quoteQty": "5.37600",
          "commission": "0.00215039",
          "commissionAsset": "USDT",
          "time": 1682283094999,
          "positionSide": "BOTH",
          "buyer": false,
          "maker": false
       },
       {
          "symbol": "ADAUSDT",
          "id": 910565858,
          "orderId": 31480052851,
          "side": "SELL",
          "price": "0.38390",
          "qty": "14",
          "realizedPnl": "0",
          "marginAsset": "USDT",
          "quoteQty": "5.37460",
          "commission": "0.00214984",
          "commissionAsset": "USDT",
          "time": 1682285029579,
          "positionSide": "BOTH",
          "buyer": false,
          "maker": false
       }
    ]
    """

    # -------------------------------------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/userTrades"
    api_key = os.getenv("api_key")
    secret_key = os.getenv("secret_key")
    parameters = {
        "symbol": symbol.upper(),
        "orderId": order_id,
        "startTime": start_time,
        "endTime": end_time,
        "fromId": from_id,
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
        return {"status_code": response.status_code, "result": result}
    else:
        return {"status_code": response.status_code, "code_error": result['code'], "text_error": result['msg']}


if __name__ in "__main__":

    get_trades(symbol="ADAUSDT", time_stamp=str(round(time.time() * 1000)))
